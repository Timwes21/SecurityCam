from deepface import DeepFace
from PIL import Image
import io
from scipy.spatial.distance import cosine
import numpy as np
from .redis_channels import set_detection


def recognize_faces(frame, username, camera_name, user_embeddings):
    frame_resized = Image.fromarray(frame).resize((112, 112))  
    frame = np.array(frame_resized)
    frame_embedding = DeepFace.represent(img_path=frame, model_name="ArcFace", enforce_detection=False)[0]["embedding"]
    on_screen = "unknown"
    
    for name, stored_embedding in user_embeddings.items():
        try:
            distance = cosine(frame_embedding, stored_embedding)
        except:
            print("not being defined")
        if distance < .03:
            on_screen = name
        print(name)

    set_detection(username, camera_name, on_screen)
    
    

def create_embedding(image_bytes_list):
    
    embeddings = []
    for i, image_bytes in enumerate(image_bytes_list):
        Image.init()
        Image.register_extension("JPEG", ".jfif")
        image = Image.open(io.BytesIO(image_bytes))
        image = image.resize((112, 112))
        image_np = np.array(image)
        embedding = DeepFace.represent(img_path=image_np, model_name="ArcFace")[0]["embedding"]
        embedding_array = np.array(embedding)
        embeddings.append(embedding_array)

    return np.mean(embeddings, axis=0)





