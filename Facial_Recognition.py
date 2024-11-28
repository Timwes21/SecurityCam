import cv2
import time
import requests
from flask import Flask, Response
import threading

app = Flask(__name__)

# telegram info
token_id = "7746370325:AAEv9KOxZxSXh-2bgzIVpF4ZsyTRdzk0irE"
chat_id = "7250352955"




cap = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(1)
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt.xml")
eye_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
faces = []
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('Tim.yml')


def telegram(message):
    url = f"https://api.telegram.org/bot{token_id}/sendMessage"
    params = {"chat_id": chat_id, "text": message}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("Notification sent successfully!")
    else:
        print(f"Failed to send notification. Error: {response.text}")




def face_detection(video):
    gray_image = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)
    face = face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=8, minSize=(40, 40))
    for (x, y, w, h) in face:
        roi_gray = gray_image[y:y+h, x:x+w]
        id_, confidence = recognizer.predict(gray_image[y:y + h, x:x + w])
        print(confidence)
        if confidence < 100:
            if "Timothy" not in faces:
                faces.append("Timothy")
        else:
            eyes = eye_classifier.detectMultiScale(roi_gray)
            if len(eyes) % 2 == 0:
                if "Unknown" not in faces:
                    faces.append("Unknown")


def stream_cam():
    while True:
        ret, frame = cap2.read()
        if not ret:
            print("this didnt work")
            exit()


        _, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
start = time.perf_counter()//2
later = start + 5 #seconds = 10 * 2
def security():
    while True:
        ret, frame = cap.read()
        now = time.perf_counter() // 2
        face_detection(frame)
        if now > later:
            if len(faces) > 0:
                telegram("In the last 15 minutes: " + str(faces))
                faces.clear()
            start = time.perf_counter() // 2
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


@app.route('/')
def home():
    return "<h1>Video Stream</h1><p>Go to <a href='/video'>/video</a> to view the video stream.</p>"

@app.route('/video')
def stream():
    return Response(stream_cam(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    camera_thread = threading.Thread(target=security, daemon=True)
    camera_thread.start()
    app.run(debug=True)
