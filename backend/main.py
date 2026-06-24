from fastapi import FastAPI
from backend.routes.health import router as health_router
from backend.routes.upload import router as upload_router
from backend.routes.evaluate import router as evaluate_router
from backend.routes.status import router as status_router
from backend.routes.results import router as results_router 
from backend.routes.download import router as download_router
from backend.routes.job import router as job_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Resume Screening API"
)

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(evaluate_router)
app.include_router(status_router)
app.include_router(results_router)
app.include_router(download_router)
app.include_router(job_router)

origins = ["https://ai-resume-intelligence-system.vercel.app"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # dev only
    allow_credentials=True,
    allow_methods=['GET','POST'],
    allow_headers=["*"],
)
