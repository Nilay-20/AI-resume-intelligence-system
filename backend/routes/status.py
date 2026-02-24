from fastapi import APIRouter
from backend.jobs.job_manager import get_job

router = APIRouter(
    prefix="/evaluation",
    tags=["Evaluation"]
)


@router.get("/status/{job_id}")
def check_status(job_id: str):

    job = get_job(job_id)

    if not job:
        return {"error": "Invalid job id"}

    return job