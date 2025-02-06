from utils.supabase_storage import save_picture
from utils.facial_rec import create_embedding

class User:
    cameras = []
    recognizable_people = []
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

    def add_a_face(self, name):
        create_embedding(self.recent_photo, name, self.username)

    def set_temporary_photo(self, image_bytes):
        self.recent_photo = image_bytes


    def save_photo(self):
        save_picture(self.username, self.recent_photo)
        self.recent_photo = None 
    
    def get_embedings(self, name, files):
        embeddings = create_embedding(files)
        for camera in self.cameras:
            camera.add_embeddings(name, embeddings)
        