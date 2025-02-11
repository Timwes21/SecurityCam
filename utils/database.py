from users import new_user

def find_user(users, username):
    for user in users:
            if user.username == username:
                return user
            
def find_camera(user, camera_name):
    for camera in user.cameras:
            if camera.name == camera_name:
                return camera




me = new_user("timwes21", "jordan18")
# simulated db for prototyping
users = [me]        

# simulated db for prototyping
detections = {"timwes21": {}}
def set_detection(username, camera, detected):
    detections[username][camera] = [detected]

def get_detection(username, camera):
    return detections[username][camera]


     