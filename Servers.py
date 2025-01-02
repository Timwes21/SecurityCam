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



@app.post("/buttons")
async def button_pressed(request: Request):
    data = await request.json()
    print(data)
    return {"message": "Button pressed!", "data": data}

@app.post("/login")
async def login(request: Request):
    data = await request.json()
    message = "Login failed!"
    for user in users:
        if user.username == data["username"] and user.password == data["password"]:
            message = "Login successful!"
            break
    return {"message": message}

    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)