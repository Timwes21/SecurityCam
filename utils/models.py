from pydantic import BaseModel

class UserModel(BaseModel):
    username: str
    password: str


class CameraModel(BaseModel):
    username: str
    ip_address: str
    name: str
    port: str

class ButtonsModel(BaseModel):
    username: str
    button_pressed: str
    camera_name: str