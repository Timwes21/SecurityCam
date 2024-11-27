import cv2
import time
import requests

# telegram info
token_id = "7746370325:AAEv9KOxZxSXh-2bgzIVpF4ZsyTRdzk0irE"
chat_id = "7250352955"


unknown_persons = "Someone is in your room"

cap = cv2.VideoCapture(1)
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt.xml")
eye_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('assets/Tim.yml')


def telegram(message):
    url = f"https://api.telegram.org/bot{token_id}/sendMessage"
    params = {"chat_id": chat_id, "text": message}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("Notification sent successfully!")
    else:
        print(f"Failed to send notification. Error: {response.text}")

start = time.perf_counter()//2
later = start + 10


def face_detection(video, now, later):
    gray_image = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)
    face = face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=8, minSize=(40, 40))
    for (x, y, w, h) in face:
        roi_gray = gray_image[y:y+h, x:x+w]
        id_, confidence = recognizer.predict(gray_image[y:y + h, x:x + w])
        print(confidence)
        if confidence < 100:
            cv2.putText(frame, "Timothy", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            if now > later:
                telegram("You are on camera!")
                return True

        else:
            eyes = eye_classifier.detectMultiScale(roi_gray)
            if len(eyes) % 2 == 0:
                #send_telegram_message(unknown_persons)
                cv2.putText(frame, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 255, 0), 2)


start = time.perf_counter()//2
later = start
while True:
    ret, frame = cap.read()
    if not ret:
        print("this didnt work")
        exit()
    now = time.perf_counter()//2


    showing = face_detection(frame, now, later)
    if showing:
        start = now
        later = start + 20
        showing = False
    frame = cv2.imshow("Detecting faces", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

