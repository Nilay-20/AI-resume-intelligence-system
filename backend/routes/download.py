from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from backend.jobs.job_manager import get_job
import os

router = APIRouter(
    prefix="/evaluation",
    tags=["Evaluation"]
)


@router.get("/download/{job_id}")
def download_csv(job_id: str):
    """
    Download evaluation CSV report
    """

    job = get_job(job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Invalid job id"
        )

    if job["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail="Evaluation not completed yet"
        )

    csv_path = job["result"]["csv_path"]

    if not os.path.exists(csv_path):
        raise HTTPException(
            status_code=404,
            detail="CSV file not found"
        )

    return FileResponse(
        path=csv_path,
        filename=os.path.basename(csv_path),
        media_type="text/csv"
    )