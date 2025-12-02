import cv2
import numpy as np
import onnxruntime as ort
import os
from typing import List, Tuple, Optional

class FaceRecognizer:
    def __init__(self, model_dir: str = "models"):
        self.model_dir = model_dir
        self.det_model_path = os.path.join(model_dir, "det_10g.onnx")
        self.rec_model_path = os.path.join(model_dir, "w600k_r50.onnx")
        self.kps_model_path = os.path.join(model_dir, "2d106det.onnx") # Landmarks if needed

        # Initialize ONNX sessions
        providers = ['CPUExecutionProvider'] # Add 'CUDAExecutionProvider' if GPU available
        
        try:
            self.det_session = ort.InferenceSession(self.det_model_path, providers=providers)
            self.rec_session = ort.InferenceSession(self.rec_model_path, providers=providers)
            print("Models loaded successfully.")
        except Exception as e:
            print(f"Error loading models: {e}")
            raise

    def preprocess(self, image: np.ndarray) -> np.ndarray:
        # Basic preprocessing for ArcFace
        # Resize to 112x112 and normalize
        # This is a simplified placeholder. Real implementation needs alignment.
        img = cv2.resize(image, (112, 112))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.transpose(img, (2, 0, 1))
        img = np.expand_dims(img, 0)
        img = (img - 127.5) / 128.0
        return img.astype(np.float32)

    def get_embedding(self, image: np.ndarray) -> Optional[np.ndarray]:
        """
        Get face embedding from an aligned face image.
        """
        try:
            input_blob = self.preprocess(image)
            input_name = self.rec_session.get_inputs()[0].name
            embedding = self.rec_session.run(None, {input_name: input_blob})[0]
            return embedding.flatten()
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return None

    def compute_similarity(self, embed1: np.ndarray, embed2: np.ndarray) -> float:
        """
        Compute cosine similarity between two embeddings.
        """
        return np.dot(embed1, embed2) / (np.linalg.norm(embed1) * np.linalg.norm(embed2))

    def detect_faces(self, image: np.ndarray, threshold: float = 0.5) -> List[dict]:
        """
        Detect faces using SCRFD (det_10g.onnx).
        Returns a list of dicts with 'bbox' and 'kps'.
        """
        # Resize and pad image to expected input size (e.g., 640x640)
        # For this example, we assume the model expects 640x640
        input_size = (640, 640)
        im_ratio = float(image.shape[0]) / image.shape[1]
        model_ratio = float(input_size[1]) / input_size[0]
        
        if im_ratio > model_ratio:
            new_height = input_size[1]
            new_width = int(new_height / im_ratio)
        else:
            new_width = input_size[0]
            new_height = int(new_width * im_ratio)
            
        det_scale = float(new_height) / image.shape[0]
        resized_img = cv2.resize(image, (new_width, new_height))
        det_img = np.zeros((input_size[1], input_size[0], 3), dtype=np.uint8)
        det_img[:new_height, :new_width, :] = resized_img
        
        input_blob = cv2.cvtColor(det_img, cv2.COLOR_BGR2RGB)
        input_blob = np.transpose(input_blob, (2, 0, 1))
        input_blob = np.expand_dims(input_blob, 0).astype(np.float32)

        input_name = self.det_session.get_inputs()[0].name
        outputs = self.det_session.run(None, {input_name: input_blob})

        # SCRFD outputs: score_8, score_16, score_32, bbox_8, bbox_16, bbox_32, kps_8, kps_16, kps_32
        # Indices depend on model export. Usually:
        # 0: score_8, 1: score_16, 2: score_32
        # 3: bbox_8, 4: bbox_16, 5: bbox_32
        # 6: kps_8, 7: kps_16, 8: kps_32
        
        scores_list = outputs[:3]
        bboxes_list = outputs[3:6]
        kpss_list = outputs[6:9]
        
        fmc = 3
        feat_stride_fpn = [8, 16, 32]
        num_anchors = 2
        
        center_cache = {}
        
        proposals = []
        
        for idx, stride in enumerate(feat_stride_fpn):
            scores = scores_list[idx][0]
            bbox_preds = bboxes_list[idx][0]
            kps_preds = kpss_list[idx][0]
            
            height, width = scores.shape
            key = (height, width, stride)
            
            if key in center_cache:
                anchor_centers = center_cache[key]
            else:
                anchor_centers = np.stack(np.mgrid[:height, :width][::-1], axis=-1).astype(np.float32) * stride
                center_cache[key] = anchor_centers

            # Filter by threshold
            pos_inds = np.where(scores >= threshold)
            if len(pos_inds[0]) == 0:
                continue
                
            scores = scores[pos_inds]
            anchor_centers = anchor_centers[pos_inds]
            bbox_preds = bbox_preds[pos_inds]
            kps_preds = kps_preds[pos_inds]
            
            # Decode bbox
            x1 = anchor_centers[:, 0] - bbox_preds[:, 0] * stride
            y1 = anchor_centers[:, 1] - bbox_preds[:, 1] * stride
            x2 = anchor_centers[:, 0] + bbox_preds[:, 2] * stride
            y2 = anchor_centers[:, 1] + bbox_preds[:, 3] * stride
            
            bboxes = np.stack([x1, y1, x2, y2], axis=-1)
            
            # Decode kps
            kps = []
            for k in range(5):
                kx = anchor_centers[:, 0] + kps_preds[:, k * 2] * stride
                ky = anchor_centers[:, 1] + kps_preds[:, k * 2 + 1] * stride
                kps.append(np.stack([kx, ky], axis=-1))
            kps = np.stack(kps, axis=1)
            
            # Combine
            for i in range(len(scores)):
                proposals.append({
                    'score': float(scores[i]),
                    'bbox': bboxes[i] / det_scale,
                    'kps': kps[i] / det_scale
                })
                
        # NMS (simplified)
        proposals.sort(key=lambda x: x['score'], reverse=True)
        keep = []
        while len(proposals) > 0:
            best = proposals.pop(0)
            keep.append(best)
            # Remove overlaps
            # ... (omitted for brevity, assuming low density or accepting overlaps for now)
            # Real implementation needs proper NMS
            
        return keep

    def align_face(self, image: np.ndarray, kps: np.ndarray) -> np.ndarray:
        # Use kps to align face to 112x112
        # Standard 5 points for ArcFace
        # Reference points for 112x112
        ref_pts = np.array([
            [38.2946, 51.6963],
            [73.5318, 51.5014],
            [56.0252, 71.7366],
            [41.5493, 92.3655],
            [70.7299, 92.2041]
        ], dtype=np.float32)
        
        tform = cv2.estimateAffinePartial2D(kps, ref_pts)[0]
        output = cv2.warpAffine(image, tform, (112, 112))
        return output


