from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to Vercel domain
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure uploads directory exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/chat")
async def chat_endpoint(
    message: str = Form(None),
    screenshot: UploadFile = File(None)
):
    file_info = None

    if screenshot:
        ext = screenshot.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(await screenshot.read())

        file_info = {
            "filename": screenshot.filename,
            "saved_as": filename
        }

    return {
        "reply": "Hi, thanks for reaching out. Your issue has been noted.",
        "file_received": bool(screenshot),
        "file_info": file_info
    }
