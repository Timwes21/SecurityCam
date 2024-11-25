import cv2
import requests

# telgram info
token_id = "7746370325:AAEv9KOxZxSXh-2bgzIVpF4ZsyTRdzk0irE"
chat_id = "7250352955"

cap = cv2.VideoCapture(1)
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
def send_telegram_message(message):
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
        eyes = eye_classifier.detectMultiScale(roi_gray)

        if len(eyes) % 2 == 0 :
            return True
        else:
            return False
    else:
        return False


while True:
    ret, frame = cap.read()
    if not ret:
        print("this didnt work")
        exit()

    showing = face_detection(frame)

    if showing:
        send_telegram_message("someone is in your room")

    cv2.imshow("Detecting faces", frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

