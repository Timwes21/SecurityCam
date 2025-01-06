from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from Security_Camera import stream, notifications_and_times
from users import User
import json


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

@app.get("/notifs")
async def get_notifications():
    return notifications_and_times



@app.post("/cameras")
async def video_feed(request: Request):
    data = await request.json()
    ip_address = data["ip_address"]
    username = data["username"]
    for user in users:
        if user.username == username:
            user.add_camera(ip_address)
            user.activate_camera()



@app.post("/phone-number")
async def phone_numbers(request: Request):
    data = await request.json()
    username = data["username"]
    phone_number = data["phone_number"]
    for user in users:
        if user.username == username:
            user.notifications.append(phone_number)
            break

@app.post("/buttons")
async def button_pressed(request: Request):
    data = await request.json()
    username = data["username"]
    button_pressed = data["button_pressed"]
    for user in users:
        if user.username == username:
            if button_pressed == "refresh":
                user.refresh_cameras()
            elif button_pressed == "notif switch":
                user.set_notifications()
            elif button_pressed == "fr switch":
                user.facial_recogintion()
            break

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

    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)