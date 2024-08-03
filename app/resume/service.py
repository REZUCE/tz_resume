import os
from dataclasses import dataclass

import aiofiles
from fastapi import UploadFile, HTTPException, status
import logging

from app.resume.repository import ResumeRepository
from app.resume.schema import ResumeCreateSchema, ResumeSchema, PagingResponseSchema
from app.settings import WorkFile

logger = logging.getLogger(__name__)


@dataclass
class ResumeService:
    resume_repository: ResumeRepository

    async def save_file(self, file: UploadFile, filename: str) -> str:
        # Создаем абсолютный путь к файлу
        file_path = os.path.join(WorkFile().FILES_PATH, filename)
        absolute_file_path = os.path.abspath(file_path)
        if os.path.exists(absolute_file_path):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A file with this name already exists. Please rename the file and try again."
            )
        os.makedirs(WorkFile().FILES_PATH, exist_ok=True)
        try:
            async with aiofiles.open(absolute_file_path, 'wb') as out_file:
                # Чтение файла по частям позволяет вашему приложению эффективно обрабатывать
                # большие файлы без излишней нагрузки на память.
                while chunk := await file.read(1024):
                    await out_file.write(chunk)
            logger.info(f"File saved at: {absolute_file_path}")
            return absolute_file_path
        except Exception as e:
            logger.error(f"An error occurred while saving the file: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while saving the file: {str(e)}"
            )

    async def create_resume(self, body: ResumeCreateSchema, file_path: str) -> ResumeSchema:
        resume = await self.resume_repository.create_resume(resume_data=body, file_path=file_path)
        resume_schema = ResumeSchema.model_validate(resume)
        return resume_schema

    async def list_resume(self, offset: int = 0, limit: int = 10) -> PagingResponseSchema[ResumeSchema]:
        resumes, total_count = await self.resume_repository.list_resumes(offset=offset, limit=limit)
        resume_schemas = [ResumeSchema.model_validate(resume) for resume in resumes]
        return PagingResponseSchema[ResumeSchema](total=total_count, items=resume_schemas, limit=limit, offset=offset)

    async def delete_resume(self, resume_id: int):
        resume = await self.resume_repository.get_resume(resume_id)
        file_path = resume.file_path
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"File deleted at: {file_path}")
            return {"message": "Resume deleted successfully"}
        else:
            logger.warning(f"File not found at: {file_path}")

        await self.resume_repository.delete_resume(resume_id)

    async def update_resume_rating(self, resume_id: int, rating: int) -> ResumeSchema:
        updated_resume = await self.resume_repository.update_resume_rating(resume_id, rating)
        return ResumeSchema.model_validate(updated_resume)