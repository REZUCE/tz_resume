from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database import get_db_session
from app.resume.repository import ResumeRepository
from app.resume.service import ResumeService


async def get_resume_repository(
        db_session: AsyncSession = Depends(get_db_session)
) -> ResumeRepository:
    return ResumeRepository(
        db_session=db_session
    )


async def get_resume_service(
        resume_repository: ResumeRepository = Depends(get_resume_repository)
) -> ResumeService:
    return ResumeService(resume_repository=resume_repository)
