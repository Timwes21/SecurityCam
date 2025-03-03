from utils import save_picture

class User:
    cameras = []
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.recent_photo = None

    def add_camera(self, ip_address, camera_name, port):
        self.cameras[camera_name] = [ip_address, port]


    def delete_camera(self, camera_name):
        for cam in self.cameras:
            if cam.name == camera_name:
                cam.stop()
                self.cameras.remove(cam)

    def get_recent_photo(self):
        return self.recent_photo

    def set_temporary_photo(self, image_bytes):
        if image_bytes is None:
            raise ValueError("recent photo is None")
        self.recent_photo = image_bytes
        if self.recent_photo is None:
            raise ValueError("recent photo is None")

    def add_a_face(self, embedding, name):
        for camera in self.cameras:
            camera.add_embeddings(embedding, name)

    def save_photo(self):
        save_picture(self.username, self.recent_photo)
        self.recent_photo = None 
    
        
def new_user(username, password):
    return User(username, password)