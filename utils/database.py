# from users import new_user
from sqlalchemy import create_engine, text
import pickle 
engine = create_engine("sqlite:///users.db", connect_args={"check_same_thread": False})

def find_user(username):
    with engine.connect() as con: 
        serialized_user = con.execute(text("SELECT data FROM another WHERE username = :username"), {"username": username})
        return pickle.loads(serialized_user[0])


def find_camera(user, camera_name):
    for camera in user.cameras:
            if camera.name == camera_name:
                return camera
            
def new_user():
     




# me = new_user("timwes21", "jordan18")
# # simulated db for prototyping
# users = [me]        

# # simulated db for prototyping
# detections = {"timwes21": {}}
# def set_detection(username, camera, detected):
#     detections[username][camera] = [detected]

# def get_detection(username, camera):
#     return detections[username][camera]


     