import bcrypt
from users import User
from .database import users


def encrypt_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def authenticate(username, password):
    for user in users:
        if user.username == username and verify_password(password, user.password):
            return "Login successful!"


