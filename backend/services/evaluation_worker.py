from app.pipeline import run_evaluation
from backend.jobs.job_manager import (
    update_job,
    update_progress
)


def evaluation_task(job_id, job_description):

    def progress(status, message):
        update_progress(job_id, status, message)

    result = run_evaluation(
        job_description,
        job_id,
        progress_callback=progress
    )

    update_job(job_id, result)