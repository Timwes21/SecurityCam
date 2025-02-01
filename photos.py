class Photo:
    def __init__(self, photo_encoded, time, camera_name):
        self.photo = photo_encoded
        self.time = time
        self.camera_name = camera_name

    def to_list(self):
        return [self.photo, self.time, self.camera_name]