import cv2
import numpy as np


# Prepare the face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Load the pre-trained face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Prepare the image
img = cv2.imread("assets/meagain.png")  # Replace with your image file name

# Check if the image was loaded successfully
if img is None:
    print("Error: Could not load image.")
    exit()

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# If faces are detected, proceed with training
if len(faces) == 0:
    print("No faces found in the image.")
else:
    # Assuming there's only one face, extract the ROI for training
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]

    # Train the recognizer using this image (you can use multiple faces for a dataset)
    recognizer.train([roi_gray], np.array([0]))  # '0' is the label for this face
    recognizer.save('Tim.yml')  # Save the trained model
    print("Training complete!")