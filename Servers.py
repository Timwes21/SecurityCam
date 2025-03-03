from fastapi import FastAPI, HTTPException, UploadFile, Response, WebSocket, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from Camera import new_camera, stream, snap
from utils import (
    encrypt_password, authenticate,
    UserModel, ButtonsModel, CameraModel,
    set_new_user, set_temporary_photo, save_temporary_photo, save_embedding,
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

cameras = {"jojo": []}

def find_camera(username, camera_name):
    for cam in cameras[username]:
            if cam.name == camera_name:
                return cam

@app.websocket("/detections/{username}/{camera_name}")
async def get_detections_websocket(websocket: WebSocket, username: str, camera_name: str):
    await websocket.accept()
    result = get_detection(username, camera_name)
    print(result)
    await websocket.send_text(get_detection(username, camera_name))


@app.post("/add-camera")
async def video_feed(cam: CameraModel):
    camera = new_camera(cam.username, cam.name, cam.ip_address, cam.port)
    cameras[cam.username].append(camera)
    camera.start()

@app.post("/login")
async def login(possible_user: UserModel):
    results = authenticate(possible_user.username, possible_user.password)
    return results


@app.post("/new-user")
async def new_user(user: UserModel):
    password = encrypt_password(user.password)
    res = set_new_user(user.username, password)
    cameras[user.username] = []
    return res

@app.get("/load-camera/{username}")
def load_camera(username: str):
    user_cameras = cameras[username]
    cam_info = [cam.get_cam_info() for cam in user_cameras]
    return cam_info
        


@app.get("/delete-camera/{username}/{camera}")
async def delete_camera(username: str, camera: str):
    cam = find_camera(username, camera)
    cam.stop()
    cameras[username].remove(cam)

@app.get("/camera/{username}/{camera_name}")
def cam(username: str, camera_name: str):
    camera = find_camera(username, camera_name)
    return StreamingResponse(stream(camera), media_type="multipart/x-mixed-replace; boundary=frame")
    

@app.get("/snap/{username}/{camera_name}")
def snap_pic(username: str, camera_name: str):
    camera = find_camera(username, camera_name)
    if not camera:
        raise HTTPException(status_code=404, detail="No Camera Selected")     
    image_bytes = snap(camera)
    set_temporary_photo(username, image_bytes)
    if not image_bytes:
        raise HTTPException(status_code=404, detail="No Photo Taken")
    return Response(snap(camera), media_type="image/jpeg")

@app.get("/save-photo/{username}")
def save_photo(username: str):
    save_temporary_photo(username)


@app.post("/buttons")
async def buttons(button: ButtonsModel):
    camera = find_camera(button.username, button.camera_name)
    camera.switch(button.button_pressed)


@app.post("/upload-photos/{username}/{name}")
async def upload_photos(username: str, name: str, files: List[UploadFile] = File(...)):
    image_bytes_list = [await file.read() for file in files]
    embedding = create_embedding(image_bytes_list)
    if not len(embedding):
        return {"message": "Could not get model from photo(s)"}
    save_embedding(username, name, embedding)
    



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)