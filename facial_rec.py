import cv2
import numpy as np
from insightface.app import FaceAnalysis

app = FaceAnalysis(name='buffalo_1', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))


def add_known_person(name: str, image_bytes: bytes):
    known_face_encodings = []
    known_face_names = []

    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    faces = app.get(image)
    if faces:
        known_face_encodings.append(faces[0].embedding)
        known_face_names.append(name)

    return known_face_encodings, known_face_names


def recognize_faces(frame, known_faces):
    faces = app.get(frame)
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