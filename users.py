import concurrent.futures
import datetime
import threading

class User:
    cameras = []
    photos = []
    people = {}
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def add_camera(self, ip_address, camera_name, port):
        self.cameras[camera_name] = [ip_address, port]


    def delete_camera(self, camera_name):
        for cam in self.cameras:
            if cam.name == camera_name:
                cam.stop()
                self.cameras.remove(cam)

    def add_people(self, name, picture):
        for camera in self.cameras:
            camera.add_person(name, picture)