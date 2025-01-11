import cv2
import asyncio
import json
import datetime
import time



datetime_function = datetime.datetime.now()
people_detected = []
notifications = {
    1: {},
    2: {},
    3: {},
    4: {}
}
time_of_notifs = []
notifications_and_times = [notifications, time_of_notifs]
wait_period = (60 * 15) # roughly every 15 minutes 
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

# API key: SecurityBotChat
        
        
def facial_rec(image_path, labels, person):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    
def manage_notifications(later, now, desired_amount_of_notifs, camera_number):
    if len(people_detected) > 0 and later < now:
        notif = f"People detected: {people_detected} on camera {camera_number}"
        time_of_notif = datetime_function.strftime("%Y-%m-%d %H:%M:%S")
        notifications.append(notif)
        time_of_notifs.append(time_of_notif)
        send_message(notif)
        people_detected.clear()
        later = now + wait_period 
    else:
        later = later
    if len(notifications) > desired_amount_of_notifs:
        notifications.pop(0)
    return later




async def stream(ip_address, camera_number):
    now = time.perf_counter()
    later = now + wait_period
    cap = cv2.VideoCapture(f"http://{ip_address}/video")
    while True:
        now = time.perf_counter()
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            continue
        
        later = manage_notifications(later, now, 20, camera_number)
        
 

def stream_puter():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        print("computer camera is being streamedS")

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')