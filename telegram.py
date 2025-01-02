import requests
import asyncio
import time

token_id = "7746370325:AAEv9KOxZxSXh-2bgzIVpF4ZsyTRdzk0irE"
chat_id = "7250352955"
url = f"https://api.telegram.org/bot{token_id}/sendMessage"

def send_message(message):
    params = {"chat_id": chat_id, "text": message}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("Notification sent successfully!")
    else:
        print(f"Failed to send notification. Error: {response.text}")
        
def send_image(image_path):
    with open(image_path, "rb") as image_file:
        response = requests.post(url, data={"chat_id": chat_id}, files={"photo": image_file})
