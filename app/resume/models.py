from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float
from app.infrastructure.database import Base


class Resume(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, unique=True)

    candidate_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id}, candidate_name={self.candidate_name!r}, file_path={self.file_path!r}, rating={self.rating!r})>"

    def __repr__(self) -> str:
        return self.__str__()
