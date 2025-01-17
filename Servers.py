from fastapi import FastAPI, HTTPException, Request, Response, BackgroundTasks
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from users import User
from Camera import Camera, stream
import threading
import json
import cv2
camera_added = False


app = FastAPI()

me = User("timwes21", "jordan18")
# camera1 = Camera("132", "2145678", "house")
# me.cameras.append(camera1)
users = [me]




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Replace "*" with specific domains if needed.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods.
    allow_headers=["*"],  # Allows all HTTP headers.
)


@app.post("/add-camera")
async def video_feed(request: Request):
    data = await request.json()
    username = data["username"]
    ip_addrress = data['camera'][0]
    camera_name = data['camera'][1]
    port = data['camera'][2]
    camera = Camera(username, camera_name, ip_addrress, port)
    for user in users:
        if username == user.username:
            user.cameras.append(camera)
    camera.start()

@app.post("/login")
async def login(request: Request):
    data = await request.json()
    message = "Login failed!"
    for user in users:
        if user.username == data["username"] and user.password == data["password"]:
            message = "Login successful!"
            break
    return {"message": message}


@app.post("/new-user")
async def new_user(request: Request):
    data = await request.json()
    new_user = User(data["username"], data["password"])
    users.append(new_user)

@app.get("/load-camera")
def load_camera():
    list_of_cameras = []
    user_cameras = {}
    for user in users:
        username = user.username
        cameras = user.cameras
        for camera in cameras:
            list_of_cameras.append(camera.name)
        user_cameras[username] = list_of_cameras
    return user_cameras


@app.post("/delete-camera")
async def delete_camera(request: Request):
    data = await request.json()
    username = data["username"]
    camera = data["camera"]
    for user in users:
        if user.username == username:
            user.delete_camera(camera)


@app.get("/camera/{username}/{camera_name}")
def cam(username: str, camera_name: str):
        for user in users:
            if user.username == username:
                for camera in user.cameras:
                    if camera.name == camera_name:
                        return StreamingResponse(stream(camera), media_type="multipart/x-mixed-replace; boundary=frame")
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)