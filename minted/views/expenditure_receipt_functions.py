import os
import uuid
from django.conf import settings
from storages.backends.azure_storage import AzureStorage

def create_new_file_name(file):
    file_name = str(uuid.uuid4())
    file_type = os.path.splitext(file.name)[-1]
    file_name = file_name + file_type
    return file_name

def handle_uploaded_file(file):
    if not file:
        return

    if 'AZURE_ACCOUNT_NAME' in os.environ:
        link = handle_azure_file_upload(file)
        return link
    
    else:
        path = handle_local_file_upload(file)
        return path

def handle_local_file_upload(file):
    file_name = create_new_file_name(file)
    path = os.path.join(settings.UPLOAD_DIR, file_name)

    if not os.path.exists(settings.UPLOAD_DIR):
        os.mkdir(settings.UPLOAD_DIR)

    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return path

def handle_azure_file_upload(file):
    container = AzureStorage()
    file_name = create_new_file_name(file)
    link = container.save(file_name, file)
    return link

def delete_file(file):
    if 'AZURE_ACCOUNT_NAME' in os.environ:
        handle_azure_file_deletion(str(file))
    else:
        handle_local_file_deletion(file.path)

def handle_azure_file_deletion(path):
    container = AzureStorage()
    container.delete(path)

def handle_local_file_deletion(path):
    if os.path.exists(path):
            os.remove(path)