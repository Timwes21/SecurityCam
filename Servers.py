from fastapi import FastAPI, HTTPException, Request, Response, BackgroundTasks
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from users import User
from Camera import Camera, stream, snap
import datetime
import base64
from pydantic import BaseModel
import cv2
camera_added = False

def find_user(users, username):
    for user in users:
            if user.username == username:
                return user
            
def find_camera(user, camera_name):
    for camera in user.cameras:
            if camera.name == camera_name:
                return camera



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
    button: str
    camera_name: str


app = FastAPI()

me = User("timwes21", "jordan18")
users = [me]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Replace "*" with specific domains if needed.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods.
    allow_headers=["*"],  # Allows all HTTP headers.
)


@app.post("/add-camera")
async def video_feed(cam: CameraModel):
    camera = Camera(cam.username, cam.name, cam.ip_address, cam.port)
    user = find_user(users, cam.username)
    user.cameras.append(camera)
    camera.start()

@app.post("/login")
async def login(possible_user: UserModel):
    for user in users:
        if user.username == possible_user.username and user.password == possible_user.password:
            return "Login successful!"
    raise HTTPException(status_code=404, detail="Login Not Successful")

@app.post("/new-user")
async def new_user(user: UserModel):
    new_user = User(user.username, user.password)
    users.append(new_user)

@app.get("/load-camera/{username}")
def load_camera(username: str):
    cameras = []
    user = find_user(users, username)
    for camera in user.cameras:
        cameras.append(camera.get_cam_info())
    return cameras


@app.post("/delete-camera")
async def delete_camera(request: Request):
    data = await request.json()
    username = data["username"]
    camera = data["camera"]
    user = find_user(users, username)
    user.delete_camera(camera)


@app.get("/camera/{username}/{camera_name}")
def cam(username: str, camera_name: str):
    user = find_user(users, username)
    camera = find_camera(user, camera_name)
    return StreamingResponse(stream(camera), media_type="multipart/x-mixed-replace; boundary=frame")
    

@app.get("/snap/{username}/{camera_name}")
def snap_pic(username: str, camera_name: str):
    user = find_user(users, username)
    camera = find_camera(user, camera_name)
    now = datetime.datetime.now()
    formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    encoed_image = base64.b64encode(snap(camera)).decode('utf-8')
    user.photos.append((encoed_image, camera_name, formatted_datetime))
    return Response(snap(camera), media_type="image/jpeg")

@app.get("/photos/{username}")
def get_user_photos(username: str):
    user = find_user(users, username)
    return user.photos
        
@app.post("/buttons")
async def buttons(button: ButtonsModel):
    user = find_user(users, button.username)
    camera = find_camera(user, button.camera_name)
    camera.switch(button.button_pressed)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)