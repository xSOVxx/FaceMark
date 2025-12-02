import onnxruntime as ort
import numpy as np
import cv2

class ArcFace:
    def __init__(self, model_path="models/arcface_r100.onnx"):
        self.session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
        self.input_name = self.session.get_inputs()[0].name

    def preprocess(self, face):
        face = cv2.resize(face, (112, 112))
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        face = (face / 255.0 - 0.5) / 0.5
        face = face.transpose(2, 0, 1)
        return np.expand_dims(face.astype(np.float32), axis=0)

    def get_embedding(self, face):
        inp = self.preprocess(face)
        emb = self.session.run(None, {self.input_name: inp})[0]
        return emb[0] / np.linalg.norm(emb[0])
