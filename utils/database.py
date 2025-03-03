from sqlalchemy import create_engine, text
import pickle 
from .user_auth import verify_password
from .supabase_storage import save_picture
engine = create_engine("sqlite:///users.db", connect_args={"check_same_thread": False})

# with engine.connect() as con:
#     con.execute(text("""CREATE TABLE users(
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 username TEXT UNIQUE,
#                 password TEXT,
#                 temporary_photo BLOB)"""))

# with engine.connect() as con:
#     con.execute(text("""CREATE TABLE embeddings(
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 username TEXT,
#                 name TEXT,
#                 embedding BLOB,
#                 FOREIGN KEY(username) REFERENCES users(username))"""))




# with engine.connect() as con:
    # con.execute(text("""DROP TABLE IF EXISTS users"""))
    

def find_user(username):
    with engine.connect() as con: 
        serialized_user = con.execute(text("SELECT data FROM users WHERE username = :username"), {"username": username}).fetchone()
        return pickle.loads(serialized_user[0])

            
def set_new_user(username, password):
     with engine.connect() as con:
        try:
            con.execute(text("INSERT INTO users(username, password) VALUES (:username, :password)"), {"username": username, "password": password})
            con.commit()
            return 0
        except Exception as e:
            print(e)
            return 1
        
        
def authenticate(username, password):
    with engine.connect() as con:
        try:
            user_password = con.execute(text("SELECT password FROM users WHERE username = :username"), {"username": username}).fetchone()
            if user_password is None:
                return 2
            if verify_password(password, user_password):
                return 0
        except Exception as e:
            return 1
        

def set_temporary_photo(username, image_bytes):
    with engine.connect() as con:
        con.execute(text("UPDATE users SET temporary_photo = :image_bytes WHERE username = :username"), {"image_bytes": image_bytes, "username": username})
        con.commit()

def save_temporary_photo(username):
    with engine.connect() as con:
        image_bytes = con.execute(text("SELECT temporary_photo FROM users WHERE username = :username"), {"username": username}).fetchone()
        save_picture(username, image_bytes)
        con.execute(text("UPDATE users SET temporary_photo = NULL WHERE username = :username"), {"username": username})
        con.commit()
        

def save_embedding(username, name, embedding):
    with engine.connect() as con:
        con.execute(text("INSERT INTO embeddings(username, name, embedding) VALUES (:username, :name, :embedding)"), {"username": username, "name": name, "embedding": embedding})
        con.commit()

def get_embeddings(username):
    with engine.connect() as con:
        embeddings = con.execute(text("SELECT name, embedding FROM embeddings WHERE username = :username"), {"username": username}).fetchall()
        return embeddings


# me = new_user("timwes21", "jordan18")
# # simulated db for prototyping
# users = [me]        

# # simulated db for prototyping
# detections = {"timwes21": {}}
# def set_detection(username, camera, detected):
#     detections[username][camera] = [detected]

# def get_detection(username, camera):
#     return detections[username][camera]


     