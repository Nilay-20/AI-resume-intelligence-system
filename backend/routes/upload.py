from fastapi import APIRouter, UploadFile, File
from typing import List
import os
import shutil

router = APIRouter()

UPLOAD_DIR = "storage/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload-resumes")
async def upload_resumes(files: List[UploadFile] = File(...)):
    """
    Upload multiple resume PDFs
    """

    uploaded_files = []

    for file in files:
        if not file.filename.endswith(".pdf"):
            continue
        file_path = os.path.join(
            UPLOAD_DIR,
            file.filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        uploaded_files.append(file.filename)

    return {
    "message": "Upload successful",
    "total_uploaded": len(uploaded_files),
    "files": uploaded_files
    }