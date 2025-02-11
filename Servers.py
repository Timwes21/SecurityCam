from fastapi import FastAPI, HTTPException, UploadFile, Response, WebSocket
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from Camera import new_camera, stream, snap
from users import User
from utils import (
    encrypt_password, authenticate,
    UserModel, ButtonsModel, CameraModel,
    users, detections, find_camera, find_user,
    create_embedding,
    get_detection
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Replace "*" with specific domains if needed.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods.
    allow_headers=["*"],  # Allows all HTTP headers.
)


@app.websocket("/detections/{username}/{camera_name}")
async def get_detections_websocket(websocket: WebSocket, username: str, camera_name: str):
    await websocket.accept()
    await websocket.send_text(get_detection(username, camera_name))




@app.post("/add-camera")
async def video_feed(cam: CameraModel):
    camera = new_camera(cam.username, cam.name, cam.ip_address, cam.port)
    user = find_user(users, cam.username)
    user.cameras.append(camera)
    camera.start()
    detections[cam.username][cam.name] = []

@app.post("/login")
async def login(possible_user: UserModel):
    authenticate(possible_user.username, possible_user.password)
    raise HTTPException(status_code=404, detail="Login Not Successful")

@app.post("/new-user")
async def new_user(user: UserModel):
    password = encrypt_password(user.password)
    new_user = User(user.username, password)
    users.append(new_user)
    detections[user.username] = {}

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


@app.post("/buttons")
async def buttons(button: ButtonsModel):
    user = find_user(users, button.username)
    camera = find_camera(user, button.camera_name)
    camera.switch(button.button_pressed)


@app.post("/upload-photos/{username}/{name}")
async def upload_photos(username: str, name: str, files: List[UploadFile]):
    user = find_user(users, username)
    embedding = create_embedding(files)
    user.add_a_face(embedding, name)

    



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)