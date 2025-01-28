from fastapi import FastAPI, HTTPException, Request, Response, BackgroundTasks
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from users import User
from Camera import Camera, stream, snap
import datetime
import base64
import cv2
camera_added = False


app = FastAPI()

me = User("timwes21", "jordan18")
# camera1 = Camera("132", "2145678", "house")
# me.cameras.append(camera1)
users = [me]

# for getting real time updates to send the users camera name for the buttons
cameras = {"timwes21" :[]}

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
            cameras[username].append(camera_name)
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
    cameras[new_user.username] = []

@app.get("/load-camera")
def load_camera():
    return cameras


@app.post("/delete-camera")
async def delete_camera(request: Request):
    data = await request.json()
    username = data["username"]
    camera = data["camera"]
    for user in users:
        if user.username == username:
            user.delete_camera(camera)
    if camera in cameras[username]:
        cameras[username].remove(camera)


@app.get("/camera/{username}/{camera_name}")
def cam(username: str, camera_name: str):
        for user in users:
            if user.username == username:
                for camera in user.cameras:
                    if camera.name == camera_name:
                        return StreamingResponse(stream(camera), media_type="multipart/x-mixed-replace; boundary=frame")
    

@app.get("/snap/{username}/{camera_name}")
def snap_pic(username: str, camera_name: str):
    for user in users:
            if user.username == username:
                for camera in user.cameras:
                    if camera.name == camera_name:
                        now = datetime.datetime.now()
                        formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
                        encoed_image = base64.b64encode(snap(camera)).decode('utf-8')
                        user.photos.append((encoed_image, camera_name, formatted_datetime))
                        return Response(snap(camera), media_type="image/jpeg")

@app.get("/photos/{username}")
def get_user_photos(username: str):
    for user in users:
        if user.username == username:
            return user.photos
        
@app.post("/buttons")
async def buttons(request: Request):
    data = await request.json()
    username = data["username"]
    button = data["buttonPressed"]
    camera_name = data["camera"]
    for user in users:
        if user.username == username:
            for camera in user.cameras:
                if camera.name == camera_name:
                    if button == "Black and White":
                        camera.black_and_white = not camera.black_and_white


@app.get("/")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)