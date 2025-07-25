'''
import requests
import os
from django.conf import settings

def upload_image_to_supabase(file, filename):
    url = f"https://{settings.SUPABASE_PROJECT_ID}.supabase.co/storage/v1/object/public/{settings.SUPABASE_BUCKET}/{filename}"
    upload_url = f"https://{settings.SUPABASE_PROJECT_ID}.supabase.co/storage/v1/object/{settings.SUPABASE_BUCKET}/{filename}"

    headers = {
        "apikey": settings.SUPABASE_API_KEY,
        "Authorization": f"Bearer {settings.SUPABASE_API_KEY}",
        "Content-Type": "application/octet-stream"
    }

    response = requests.post(upload_url, headers=headers, data=file.read())
   
    if response.status_code == 200 or response.status_code == 201:
        return url  # public URL to the image
    else:
        raise Exception(f"Upload failed: {response.status_code} - {response.text}")
        '''