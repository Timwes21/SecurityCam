from deepface import DeepFace
from PIL import Image
import io
from scipy.spatial.distance import cosine
import numpy as np
from .database import set_detection


def recognize_faces(frame, username, camera_name, user_embeddings):
    frame = np.array(frame)
    frame_embedding = DeepFace.represent(frame, model_name="ArcFace", enforce_detection=False)[0]["embedding"]
    on_screen = "unknown"
    
    for name, stored_embedding in user_embeddings.items():
        distance = cosine(frame_embedding, stored_embedding)
        
        if distance < .06:
            on_screen = name

        
    set_detection(username, camera_name, on_screen)
    
    

def create_embedding(image_bytes_list):
    
    embeddings = []
    for image_bytes in image_bytes_list:
        image = Image.open(io.BytesIO(image_bytes))
        embedding = DeepFace.represent(img_path=image, model_name="Facenet")[0]["embedding"]
        embedding_array = np.array(embedding)
        embeddings.append(embedding_array)

    return np.mean(embeddings, axis=0)





