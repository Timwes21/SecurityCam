from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from Security_Camera import stream, notifications_and_times, stream_puter
from users import User
import json

app = FastAPI()

me = User("timwes21", "jordan18")
me.cameras["house"] = "2145678"
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
    ip_address = data["camera"][0]
    camera_name = data["camera"][1]
    for user in users:
        if user.username == username:
            user.add_camera(ip_address, camera_name)

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
    cameras = {}
    for user in users:
        username = user.username
        user_cameras = user.cameras
        cameras[username] = user_cameras
    return cameras






    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)