import uuid

jobs = {}


def create_job():
    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "status": "queued",
        "progress": "Waiting to start",
        "result": None
    }

    return job_id


def update_progress(job_id, status, message):
    jobs[job_id]["status"] = status
    jobs[job_id]["progress"] = message


def update_job(job_id, result):
    jobs[job_id]["status"] = "completed"
    jobs[job_id]["progress"] = "Evaluation completed"
    jobs[job_id]["result"] = result


def get_job(job_id):
    return jobs.get(job_id)