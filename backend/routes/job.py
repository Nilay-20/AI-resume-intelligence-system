from fastapi import APIRouter
from backend.jobs.job_manager import create_job

router = APIRouter(
    prefix="/job",
    tags=["Job"]
)


@router.post("/create")
def create_new_job():
    """
    Create new hiring session
    """

    job_id = create_job()

    return {
        "message": "Job created",
        "job_id": job_id
    }