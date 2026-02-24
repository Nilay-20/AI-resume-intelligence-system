from fastapi import APIRouter, Form, BackgroundTasks, HTTPException
from backend.jobs.job_manager import get_job
from backend.services.evaluation_worker import evaluation_task
import os

router = APIRouter(
    prefix="/evaluation",
    tags=["Evaluation"]
)


@router.post("/evaluate")
async def evaluate(
    background_tasks: BackgroundTasks,
    job_id: str = Form(...),
    job_description: str = Form(...)
):
    """
    Start evaluation for an existing job
    """

    # -----------------------------
    # Validate Job
    # -----------------------------
    job = get_job(job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Invalid job_id"
        )

    # -----------------------------
    # Validate Upload Folder
    # -----------------------------
    upload_dir = f"storage/jobs/{job_id}"

    if not os.path.exists(upload_dir):
        raise HTTPException(
            status_code=400,
            detail="No resumes uploaded for this job"
        )

    if not os.listdir(upload_dir):
        raise HTTPException(
            status_code=400,
            detail="Upload resumes before evaluation"
        )

    # -----------------------------
    # Start Background Evaluation
    # -----------------------------
    background_tasks.add_task(
        evaluation_task,
        job_id,
        job_description
    )

    return {
        "message": "Evaluation started",
        "job_id": job_id
    }