import concurrent.futures
import datetime
import threading
from photos import Photo
from supabase_storage import save_picture

class User:
    cameras = []
    people_embeddings = {"examlpe": []} 
    recent_photo = None
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

    def set_temporary_photo(self, image_bytes):
        self.recent_photo = image_bytes

    def get_people(self):
        peoples_photos = {}
        for person in self.people:
            peoples_photos[person] = []
            for photo in self.people[person]:
                peoples_photos[person].append(photo.to_list())
        return peoples_photos

    def save_photo(self):
        save_picture(self.username, self.recent_photo)
        self.recent_photo = None 
        

    def delete_photo(self, name, index):
        if name == "gallery":
            self.photos.pop(index)
        else:
            self.people[name].pop(index)