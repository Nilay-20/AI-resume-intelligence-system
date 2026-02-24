from fastapi import APIRouter, Form, BackgroundTasks
from backend.jobs.job_manager import create_job
from backend.services.evaluation_worker import evaluation_task

router = APIRouter(
    prefix="/evaluation",
    tags=["Evaluation"]
)


@router.post("/evaluate")
async def evaluate(
    background_tasks: BackgroundTasks,
    job_description: str = Form(...)
):

    job_id = create_job()

    background_tasks.add_task(
        evaluation_task,
        job_id,
        job_description
    )

    return {
        "message": "Evaluation started",
        "job_id": job_id
    }