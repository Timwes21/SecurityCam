from deepface import DeepFace
from PIL import Image
import io
from supabase_storage import get_embeddings, save_embedding
from scipy.spatial.distance import cosine


def recognize_faces(frame, username):
    frame_embedding = DeepFace.represent(frame, model_name="Facenet")[0]["embedding"]

    user_embeddings = get_embeddings(username) or {}

    best_match = None
    best_distance = float('inf')
    for name, stored_embedding in user_embeddings.items():
        distance = cosine(frame_embedding, stored_embedding)
        
        if distance < best_distance:
            best_distance = distance
            best_match = name

    if best_distance < 0.6:
        return best_match
    else:
        return "unknown"

def create_embedding(image_bytes, name, username):
    image = Image.open(io.BytesIO(image_bytes))
    embeddings = DeepFace.represent(img_path=image, model_name="Facenet")
    save_embedding(username, name, embeddings[0]["embedding"])




