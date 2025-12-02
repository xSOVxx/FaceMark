from ultralytics import YOLO
import cv2

class FaceDetector:
    def __init__(self, model_path="models/yolov8n-face.onnx"):
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model(frame, verbose=False)
        detections = []
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                detections.append([int(x1), int(y1), int(x2), int(y2)])
        return detections
