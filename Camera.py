import cv2
import threading
import queue
from facial_rec import add_known_persons, recognize_faces
import cv2
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image

app = FaceAnalysis(name='buffalo_1')
app.prepare(ctx_id=0, det_size=(640, 640))

class Camera:
    known_faces = {}
    face_names = None
    def __init__(self, username, name, ip, port):
        self.cap = cv2.VideoCapture(f"http://{ip}:{port}/video")
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
            ret, frame = self.cap.read()

            if self.facial_rec:
                self.face_names = recognize_faces(frame, self.known_face_encodings, self.known_face_names)

            if ret:
                if self.black_and_white:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if self.frame_queue.full():
                    self.frame_queue.get() 
                self.frame_queue.put(frame)

    def get_frame(self):
        return self.frame_queue.get()
    
    def get_faces(self):
        return self.face_names
    
    def switch(self, button):
        if button == "Black and White":
            self.black_and_white = not self.black_and_white

    def get_cam_info(self):
        cam_info = {"name": self.name, "Black and White": self.black_and_white}
        return cam_info
    
    def add_person(self, name, picture):
        known_person, known_embinng = add_known_persons(name, picture)
        self.known_faces[known_person] = known_embinng

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
        
