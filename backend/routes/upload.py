from fastapi import APIRouter, UploadFile, File, Form
from typing import List
import os
import shutil

router = APIRouter(prefix="/files", tags=["Upload"])


@router.post("/upload-resumes")
async def upload_resumes(
    job_id: str = Form(...),
    files: List[UploadFile] = File(...)
):

    upload_dir = f"storage/jobs/{job_id}/uploads"
    os.makedirs(upload_dir, exist_ok=True)

    uploaded = []

    for file in files:

        path = os.path.join(upload_dir, file.filename)

        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        uploaded.append(file.filename)

    return {
        "message": "Uploaded successfully",
        "job_id": job_id,
        "files": uploaded
    }