import logging
from dataclasses import dataclass

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, insert, func, update

from app.resume.models import Resume
from app.resume.schema import ResumeCreateSchema

logger = logging.getLogger(__name__)


@dataclass
class ResumeRepository:
    db_session: AsyncSession

    async def create_resume(self, resume_data: ResumeCreateSchema, file_path: str) -> Resume:
        query = insert(Resume).values(
            candidate_name=resume_data.candidate_name,
            file_path=file_path
        ).returning(Resume)
        async with self.db_session as session:
            try:
                result = await session.execute(query)
                await session.commit()
                new_resume = result.scalars().one()
                return new_resume
            except SQLAlchemyError as e:
                logger.error(f"An error occurred while creating the resume: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error occurred: {str(e)}"
                )

    async def list_resumes(self, offset: int = 0, limit: int = 10) -> (list[Resume], int):
        total_count_column = func.count(Resume.id).over().label("total_count")
        query = (
            select(Resume, total_count_column)
            .offset(offset)
            .limit(limit)
        )
        async with self.db_session as session:
            try:
                results = await session.execute(query)
                rows = results.fetchall()
                if rows:
                    resumes = [row[0] for row in rows]
                    total_count = rows[0][1]
                else:
                    resumes = []
                    total_count = 0
                return resumes, total_count
            except SQLAlchemyError as e:
                logger.error(f"An error occurred while listing resumes: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error occurred: {str(e)}"
                )

    async def get_resume(self, resume_id: int) -> Resume:
        query = select(Resume).where(Resume.id == resume_id)
        async with self.db_session as session:
            try:
                result = await session.execute(query)
                resume = result.scalars().first()
                if not resume:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
                return resume
            except SQLAlchemyError as e:
                logging.error(f"An error occurred while getting the resume: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error occurred: {str(e)}"
                )

    async def delete_resume(self, resume_id: int):
        query = delete(Resume).where(Resume.id == resume_id)
        async with self.db_session as session:
            try:
                await session.execute(query)
                await session.commit()
            except SQLAlchemyError as e:
                logging.error(f"An error occurred while deleting the resume: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error occurred: {str(e)}"
                )

    async def update_resume_rating(self, resume_id: int, rating: float) -> Resume:
        query = update(Resume).where(Resume.id == resume_id).values(rating=rating).returning(Resume)
        async with self.db_session as session:
            try:
                result = await session.execute(query)
                await session.commit()
                updated_resume = result.scalars().one()
                return updated_resume
            except SQLAlchemyError as e:
                logging.error(f"An error occurred while updating the resume rating: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error occurred: {str(e)}"
                )
