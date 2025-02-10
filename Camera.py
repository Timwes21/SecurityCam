import cv2
import threading
import queue
import cv2
from utils import recognize_faces

class Camera:
    embeddings = {}
    recent_detection = ""
    n = 0
    def __init__(self, username, name, ip, port):
        self.cap = cv2.VideoCapture(0)
        self.username = username
        self.name = name
        self.running = True
        self.black_and_white = True
        self.facial_rec = False
        self.frame_queue = queue.Queue(maxsize=10)
        self.thread = threading.Thread(target=self.update, daemon=True)

    def start(self):
        self.thread.start()

    def update(self):
        while self.running:
            self.n += 1
            ret, frame = self.cap.read()

            if self.facial_rec and self.n % 500 == 0:
                recognize_faces(frame, self.username, self.name, self.embeddings)
                self.n = 1

            if ret:
                if self.black_and_white:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if self.frame_queue.full():
                    self.frame_queue.get() 
                self.frame_queue.put(frame)

    def get_frame(self):
        return self.frame_queue.get()
    
    def add_embeddings(self, embeding, name):
        self.embeddings[name] = embeding
    
    def switch(self, button):
        if button == "Black and White":
            self.black_and_white = not self.black_and_white
        elif button == "Facial Recognition":
            self.facial_rec = not self.facial_rec

    def get_cam_info(self):
        return {"name": self.name, "Black and White": self.black_and_white, "Facial Recognition": self.facial_rec}    

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
            # Further abstraction for caution
            display_frame = frame.copy()

            ret, buffer = cv2.imencode('.jpg', display_frame)
            return buffer.tobytes()
        

