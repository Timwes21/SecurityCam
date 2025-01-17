import cv2
import asyncio
import json
import datetime
import time
from telegram import send_message
import base64



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
        
        
def facial_rec(frame, cam):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(faces) > 1:
        send_message(f"someone detected {cam}")
    
def manage_notifications(later, now, desired_amount_of_notifs, camera_number):
    if len(people_detected) > 0 and later < now:
        notif = f"People detected: {people_detected} on camera {camera_number}"
        time_of_notif = datetime_function.strftime("%Y-%m-%d %H:%M:%S")
        time_of_notifs.append(time_of_notif)
        send_message(notif)
        people_detected.clear()
        later = now + wait_period 
    else:
        later = later
    if len(notifications) > desired_amount_of_notifs:
        notifications.pop(0)
    return later




def stream(ip_address, port):
    now = time.perf_counter()
    later = now + wait_period
    cap = cv2.VideoCapture(f"http://{ip_address}:{port}/video")
    while True:
        ret, frame = cap.read()
        now = time.perf_counter()
        # facial_rec(frame)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        
        
        
 

