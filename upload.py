import os
import uuid
from fastapi import UploadFile

UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_upload(file: UploadFile) -> str:
    ext = file.filename.split(".")[-1]
    file_id = f"{uuid.uuid4()}.{ext}"
    path = os.path.join(UPLOAD_DIR, file_id)

    with open(path, "wb") as f:
        f.write(await file.read())

    return path
