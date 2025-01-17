from Security_Camera import stream
import concurrent.futures
import datetime
import threading

class User:
    cameras = []
    generating = []
    notifications = []
    phone_number = ""
    model_paths = {}
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def add_camera(self, ip_address, camera_name, port):
        self.cameras[camera_name] = [ip_address, port]
        # thread = threading.Thread(target=stream, args=(ip_address, port))
        # thread.start()

    def delete_camera(self, camera):
        self.cameras.pop(camera)