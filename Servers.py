from fastapi import FastAPI, HTTPException, UploadFile, Response, WebSocket
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from Camera import Camera, stream, snap
import asyncio
from users import User
from utils import (
    r,
    encrypt_password, verify_password,
    UserModel, ButtonsModel, CameraModel,

)

active_connections = {}

def find_user(users: list, username: str) -> User:
    for user in users:
            if user.username == username:
                return user
            
def find_camera(user: User, camera_name: str) -> Camera:
    for camera in user.cameras:
            if camera.name == camera_name:
                return camera


        

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





@app.websocket("/detections/{username}/{camera}")
async def detections(websocket: WebSocket, username: str, camera: str):
    await websocket.accept()
    channel = f"{username}:{camera}"
    active_connections[channel] = websocket

    sub = r.pubsub()
    sub.subscribe(channel)
    try:
        while True:
            message = sub.get_message(True)
            if message:
                await websocket.send_text(message["data"])
            await asyncio.sleep(0.1)
    except:
        del active_connections[channel]
        sub.unsubscribe(channel)




@app.post("/add-camera")
async def video_feed(cam: CameraModel):
    camera = Camera(cam.username, cam.name, cam.ip_address, cam.port)
    user = find_user(users, cam.username)
    user.cameras.append(camera)
    camera.start()

@app.post("/login")
async def login(possible_user: UserModel):
    for user in users:
        if user.username == possible_user.username and verify_password(possible_user.password, user.password):
            return "Login successful!"
    raise HTTPException(status_code=404, detail="Login Not Successful")

@app.post("/new-user")
async def new_user(user: UserModel):
    password = encrypt_password(user.password)
    new_user = User(user.username, password)
    users.append(new_user)

@app.get("/load-camera/{username}")
def load_camera(username: str):
    cameras = []
    user = find_user(users, username)
    for camera in user.cameras:
        cameras.append(camera.get_cam_info())
    return cameras


@app.get("/delete-camera/{username}/{camera}")
async def delete_camera(username: str, camera: str):
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
    image_bytes = snap(camera)
    user.set_temporary_photo(image_bytes)
    return Response(snap(camera), media_type="image/jpeg")

@app.get("/save-photo/{username}")
def save_photo(username: str):
    user = find_user(users, username)
    user.save_photo()


@app.get("/people/{username}/{name_of_person}")
def get_people(username: str, name_of_person: str):
    user = find_user(users, username)
    user.add_a_face(name_of_person)



@app.post("/buttons")
async def buttons(button: ButtonsModel):
    user = find_user(users, button.username)
    camera = find_camera(user, button.camera_name)
    camera.switch(button.button_pressed)


@app.post("/upload-photos/{username}")
async def upload_photos(username: str, files: List[UploadFile]):
    user = find_user(users, username)
    user.add_a_face(files)
    return {"message": "git the images!"}

    



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)