import concurrent.futures
import datetime
import threading
from photos import Photo

class User:
    cameras = []
    photos = []
    people = {"examlpe": []} 
    recent_photo = []
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

    def set_temporary_photo(self, photo, camera_name, time):
        self.recent_photo = [photo, time, camera_name]

    def get_people(self):
        return self.people

    def save_photo(self, name):
        photo = Photo(self.recent_photo[0], self.recent_photo[1], self.recent_photo[2]) 
        if name not in self.people:
            self.people[name] = [photo]
        else: 
            self.people[name].append(photo)

    def delete_photo(self, name, index):
        if name == "gallery":
            self.photos.pop(index)
        else:
            self.people[name].pop(index)