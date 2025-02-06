from supabase import create_client, Client
url = "https://wwvtvsapleldrdrblnka.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind3dnR2c2FwbGVsZHJkcmJsbmthIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQ5MjYxMjQsImV4cCI6MjA1MDUwMjEyNH0.R2XNRCLYW32M1nKKCM8-30lROLODMtwhNB3Xh3h4c7E"
supabase: Client = create_client(url, key)


def save_picture(username, image_bytes):
    images = supabase.storage.from_("user-images").list(f"{username}/")
    image_index = len(images) + 1
    supabase.storage.from_("Images").upload(f"{username}/image{image_index}.jpg", image_bytes, {"content-type": "image/jpeg"})


def update_camera(username, camera, name):
    supabase.table("on_camera").upsert({"username": username, "camera": camera, "person(s)_spotted": name})