from fastapi import FastAPI

from app.resume.handlers import router as resume_router

app = FastAPI(title="Resume")

app.include_router(resume_router)
