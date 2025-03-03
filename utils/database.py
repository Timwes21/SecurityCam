# from users import new_user
from sqlalchemy import create_engine, text
import pickle 
# from .user_auth import verify_password
engine = create_engine("sqlite:///users.db", connect_args={"check_same_thread": False})

# with engine.connect() as con:
#     con.execute(text("""CREATE TABLE users(
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 username TEXT UNIQUE,
#                 password TEXT)"""))


# with engine.connect() as con:
#     con.execute(text("""CREATE TABLE gallery(
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 username TEXT UNIQUE,
#                 camera_name TEXT,
#                 images BLOB,
#                 FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE)"""))

# with engine.connect() as con:
#     con.execute(text("""DROP TABLE IF EXISTS userstable"""))
#     con.execute(text("""DROP TABLE IF EXISTS cameras"""))
#     con.execute(text("""DROP TABLE IF EXISTS gallery"""))
#     con.execute(text("""DROP TABLE IF EXISTS users"""))
    

def find_user(username):
    with engine.connect() as con: 
        serialized_user = con.execute(text("SELECT data FROM users WHERE username = :username"), {"username": username}).fetchone()
        return pickle.loads(serialized_user[0])

            
def set_new_user(username, password):
     with engine.connect() as con:
        try:
            con.execute(text("INSERT INTO userstable(username, password) VALUES (:username, :password)"), {"username": username, "password": password})
            con.commit()
            return 0
        except Exception as e:
            print(e)
            return 1
        
        
# def authenticate(username, password):
#     with engine.connect() as con:
#         try:
#             user_password = con.execute(text("SELECT pasword FROM userstable WHERE username = :username"), {"username": username}).fetchone()
#             if user_password is None:
#                 return 2
#             if verify_password(password, user_password):
#                 return 0
#         except Exception as e:
#             return 1
        
def update_camera(username, camera, camera_name):
    with engine.connect() as con:
        camera_serialized = pickle.dumps(camera)
        con.execute(text("UPDATE cameras SET camera = :camera WHERE username = :username AND camera_name =:camera_name"), {"camera": camera_serialized, "username": username, "camera_name":camera_name})
        con.commit()
        



# me = new_user("timwes21", "jordan18")
# # simulated db for prototyping
# users = [me]        

# # simulated db for prototyping
# detections = {"timwes21": {}}
# def set_detection(username, camera, detected):
#     detections[username][camera] = [detected]

# def get_detection(username, camera):
#     return detections[username][camera]


     