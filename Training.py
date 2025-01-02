import cv2
import numpy as np

def create_person_model(name_of_person):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    img = cv2.imread("assets/meagain.png")  # Replace with your image file name
    if img is None:
        print("Error: Could not load image.")
        exit()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(faces) == 0:
        print("No faces found in the image.")
    else:
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]

        
        recognizer.train([roi_gray], np.array([0]))  
        recognizer.save(f'{name_of_person}.yml')  
        print("Training complete!")




        