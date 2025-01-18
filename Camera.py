import cv2
import time
from Security_Camera import facial_rec
import pickle
import threading
import queue
from telegram import send_message


class Camera:
    def __init__(self, username, name, ip, port):
        self.cap = cv2.VideoCapture(f"http://{ip}:{port}/video")
        self.username = username
        self.name = name
        self.running = True
        self.frame_queue = queue.Queue(maxsize=10)
        self.thread = threading.Thread(target=self.update, daemon=True)

    def start(self):
        self.thread.start()

    def update(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                if self.frame_queue.full():
                    self.frame_queue.get() 
                self.frame_queue.put(frame)

    def get_frame(self):
        return self.frame_queue.get()

    def stop(self):
        self.running = False
        self.thread.join()
        self.cap.release()





def stream(video):
    while True:
        frame = video.get_frame()
        if frame is not None:
            # Duplicate frame
            display_frame = frame.copy()

            ret, buffer = cv2.imencode('.jpg', display_frame)
            yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            
def snap(video):
    while True:
        frame = video.get_frame()
        if frame is not None:
            # Duplicate frame
            display_frame = frame.copy()

            ret, buffer = cv2.imencode('.jpg', display_frame)
            return buffer.tobytes()