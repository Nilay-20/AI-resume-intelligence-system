from fastapi import APIRouter
from backend.jobs.job_manager import get_job

router = APIRouter(
    prefix="/evaluation",
    tags=["Evaluation"]
)


@router.get("/results/{job_id}")
def get_results(job_id: str):
    """
    Retrieve evaluation results
    """

    job = get_job(job_id)

    if not job:
        return {"error": "Invalid job id"}

    if job["status"] != "completed":
        return {
            "message": "Evaluation still processing"
        }

    return {
        "status": "completed",
        "results": job["result"]["results"],
        "csv_path": job["result"]["csv_path"]
    }