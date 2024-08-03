from enum import Enum
from typing import Generic, TypeVar
from fastapi import Query
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class PagingSchema(BaseModel):
    limit: int
    offset: int


async def pagination_params(
        limit: int = Query(default=10, ge=1, le=100, reqyired=False, description="Page size limit"),
        offset: int = Query(default=0, ge=0, le=50, reqyired=False, description="Skip")
) -> PagingSchema:
    return PagingSchema(limit=limit, offset=offset)


class RatingEnum(int, Enum):
    one: int = 1
    two: int = 2
    three: int = 3
    four: int = 4
    five: int = 5


class RatingUpdateSchema(BaseModel):
    rating: RatingEnum


class PagingResponseSchema(GenericModel, Generic[T]):
    total: int
    items: list[T]
    limit: int
    offset: int

    class Config:
        arbitrary_types_allowed = True


class ResumeSchema(BaseModel):
    id: int
    candidate_name: str
    file_path: str
    rating: float | None

    class Config:
        from_attributes = True


class ResumeCreateSchema(BaseModel):
    candidate_name: str


class ResumeUpdateSchema(BaseModel):
    rating: float
