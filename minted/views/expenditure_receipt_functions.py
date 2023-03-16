import os
import uuid
from django.conf import settings

def handle_uploaded_file(file):
    """ Add file to upload directory with a unique uuid filename"""
    file_name = str(uuid.uuid4())  
    file_type = os.path.splitext(file.name)[-1]
    file_name = file_name + file_type
    path = os.path.join(settings.UPLOAD_DIR, file_name)

    if not os.path.exists(settings.UPLOAD_DIR):
        os.mkdir(settings.UPLOAD_DIR)

    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    
    return path

def delete_file(path: str):
    """ Deletes a file at a path if it exists """
    if os.path.exists(path):
        os.remove(path)