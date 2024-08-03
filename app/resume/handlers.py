import logging
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, Form, File, HTTPException, status

from app.dependency import get_resume_service
from app.resume.schema import ResumeSchema, ResumeCreateSchema, PagingSchema, PagingResponseSchema, pagination_params, \
    RatingUpdateSchema
from app.resume.service import ResumeService

router = APIRouter(prefix="/resumes", tags=["Загрузка и вывод резюме"])
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post(
    "/upload/",
    response_model=ResumeSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_resume(
        candidate_name: Annotated[str, Form(...)],
        resume_service: Annotated[ResumeService, Depends(get_resume_service)],
        file: Annotated[UploadFile, File(...)],
):
    try:
        logger.info("Starting file upload process")
        file_path = await resume_service.save_file(file, file.filename)
        resume_data = ResumeCreateSchema(candidate_name=candidate_name)
        logger.info(f"Creating resume for candidate: {candidate_name}")
        return await resume_service.create_resume(resume_data, file_path)
    except HTTPException as e:
        logger.error(f"HTTP error occurred: {str(e.detail)}")
        raise e
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.get(
    '/list/',
    response_model=PagingResponseSchema[ResumeSchema],
    status_code=status.HTTP_200_OK
)
async def list_resume(
        resume_service: Annotated[ResumeService, Depends(get_resume_service)],
        pagination: Annotated[PagingSchema, Depends(pagination_params)],

):
    try:
        return await resume_service.list_resume(offset=pagination.offset, limit=pagination.limit)
    except HTTPException as e:
        logger.error(f"HTTP error occurred: {str(e.detail)}")
        raise e
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.delete(
    "/delete/{resume_id}/",
    status_code=status.HTTP_200_OK,
    response_model=dict
)
async def delete_resume(
        resume_id: int,
        resume_service: Annotated[ResumeService, Depends(get_resume_service)],
):
    try:
        return await resume_service.delete_resume(resume_id)
    except HTTPException as e:
        logger.error(f"HTTP error occurred: {str(e.detail)}")
        raise e
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.put(
    "/{resume_id}/rate/",
    response_model=ResumeSchema,
    status_code=status.HTTP_200_OK
)
async def rate_resume(
        resume_id: int,
        rating: Annotated[RatingUpdateSchema, Depends()],
        resume_service: Annotated[ResumeService, Depends(get_resume_service)],
):
    try:
        return await resume_service.update_resume_rating(resume_id, rating.rating)
    except HTTPException as e:
        logger.error(f"HTTP error occurred: {str(e.detail)}")
        raise e
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
