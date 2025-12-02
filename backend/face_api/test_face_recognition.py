import cv2
import numpy as np
import sys
import os

# Add parent directory to path to import services
sys.path.append(os.getcwd())

from services.face_recognition import FaceRecognizer

def test_face_recognition():
    print("Initializing FaceRecognizer...")
    try:
        # Assuming models are in 'models' directory relative to current script
        fr = FaceRecognizer(model_dir="models")
        
        # Create a dummy image (640x640x3)
        dummy_img = np.zeros((640, 640, 3), dtype=np.uint8)
        
        print("Testing detection...")
        faces = fr.detect_faces(dummy_img)
        print(f"Detections: {len(faces)}")
        
        print("Testing embedding...")
        # Create a dummy aligned face (112x112x3)
        dummy_face = np.random.randint(0, 255, (112, 112, 3), dtype=np.uint8)
        emb = fr.get_embedding(dummy_face)
        
        if emb is not None:
            print(f"Embedding shape: {emb.shape}")
        else:
            print("Embedding failed")
            
        print("Test passed!")
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_face_recognition()
