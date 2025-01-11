from Security_Camera import stream, stream_puter
import datetime

class User:
    cameras = {}
    notifications = []
    phone_number = ""
    model_paths = {}
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.facial_rec = False
        self.notification_status = True


    def add_camera(self, ip_address):
        self.cameras[ip_address] = False

    def remove_camera(self, ip_address):
        self.cameras.pop(ip_address) 
    
    def activate_camera(self):
        n=1
        for camera in self.cameras:
            if self.cameras[camera] == False:
                if camera == "puter":
                    stream_puter()
                else:
                    stream(camera, n)
                self.cameras[camera] = True
            n+=1
    
    def refresh_cameras(self):
        for camera in self.cameras:
            self.cameras[camera] = False
        self.activate_camera()
    
    def set_notifications(self):
        self.notification_status = not self.notification_status
    
    def facial_recogintion(self):
        self.facial_rec = not self.facial_rec

    def train_model(self):
        pass

   
