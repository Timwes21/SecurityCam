import numpy as np
from deepface import DeepFace
import os

def add_new_person(username, person):
    os.makedirs(f"faces/{username}/{person}/", exist_ok=True)

def recognize_faces(frame, known_faces):
    faces = handler.get(frame)
    face_names = []
    known_face_names = []
    known_face_encodings = []
    
    for i, j in enumerate(known_faces):
        known_face_names.append(i), known_face_encodings.append(j)

    
    for face in faces:
        distances = np.linalg.norm(known_face_encodings - face.embedding, axis=1)
        min_distance_index = np.argmin(distances)
        if distances[min_distance_index] < 1.0:  # Threshold for face recognition
            name = known_face_names[min_distance_index]
        else:
            name = "Unknown"
        face_names.append((face.bbox, name))

    return face_names