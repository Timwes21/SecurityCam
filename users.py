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

    def add_camera(self, ip_address, camera_name):
        self.cameras[camera_name] = ip_address