from Security_Camera import stream

class User:
    cameras = {}
    notifications = []
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def add_camera(self, ip_address):
        self.cameras[ip_address] = False

    def remove_camera(self, ip_address):
        self.cameras.pop(ip_address)
    
    def activate_camera(self):
        n=1
        for camera in self.cameras:
            if self.cameras[camera] == False:
                stream(camera, n)
                self.cameras[camera] = True
            n+=1
    
    def refresh_cameras(self):
        for camera in self.cameras:
            self.cameras[camera] = False
        self.activate_camera()
    

    
    

