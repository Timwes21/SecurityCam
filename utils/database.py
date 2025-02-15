# from users import new_user
from sqlalchemy import create_engine, text
import pickle 
from .user_auth import verify_password
engine = create_engine("sqlite:///users.db", connect_args={"check_same_thread": False})

# with engine.connect() as con:
#     con.execute(text("""CREATE TABLE users(
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 username TEXT UNIQUE,
#                 data BLOB)"""))


def find_user(username):
    with engine.connect() as con: 
        serialized_user = con.execute(text("SELECT data FROM users WHERE username = :username"), {"username": username}).fetchone()
        return pickle.loads(serialized_user[0])


def find_camera(user, camera_name):
    for camera in user.cameras:
            if camera.name == camera_name:
                return camera
            
def set_new_user(new_user):
     new_user_serialized = pickle.dumps(new_user) 
     with engine.connect() as con:
        try:
            con.execute(text("INSERT INTO users(username, data) VALUES (:username, :user)"), {"username": new_user.username, "user": new_user_serialized})
            con.commit()
            return 0
        except Exception as e:
            print(e)
            return 1
        
        
def authenticate(username, password):
    with engine.connect() as con:
        try:
            serialized_user = con.execute(text("SELECT data FROM users WHERE username = :username"), {"username": username}).fetchone()
            if serialized_user is None:
                return 2
            user = pickle.loads(serialized_user[0])
            if user.username == username and verify_password(password, user.password):
                return 0
        except Exception as e:
            return 1
        



# me = new_user("timwes21", "jordan18")
# # simulated db for prototyping
# users = [me]        

# # simulated db for prototyping
# detections = {"timwes21": {}}
# def set_detection(username, camera, detected):
#     detections[username][camera] = [detected]

# def get_detection(username, camera):
#     return detections[username][camera]


     