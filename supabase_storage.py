from supabase import create_client, Client
url = "https://wwvtvsapleldrdrblnka.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind3dnR2c2FwbGVsZHJkcmJsbmthIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQ5MjYxMjQsImV4cCI6MjA1MDUwMjEyNH0.R2XNRCLYW32M1nKKCM8-30lROLODMtwhNB3Xh3h4c7E"
supabase: Client = create_client(url, key)


def save_picture(image_bytes):
    supabase.storage.from_("images").upload(file_path, image_bytes, {"content-type": "image/jpeg"})