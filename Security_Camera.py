import cv2
import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import threading

app = FastAPI()


cap = cv2.VideoCapture(0)

async def security():
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            continue

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        await asyncio.sleep(0.01)  


@app.get("/video")
async def video_feed():
    return StreamingResponse(security(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/")
async def index():
    return '''
    <html>
        <body>
            <h1>Live Video Stream</h1>
            <img src="/video" width="640" height="480">
        </body>
    </html>
    '''

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)