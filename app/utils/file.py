import aiofiles

from app.settings import WorkFile
import os
from fastapi import HTTPException, status


async def save_file(file, filename: str) -> str:
    file_path = os.path.join(WorkFile().FILES_PATH, filename)
    os.makedirs(WorkFile().FILES_PATH, exist_ok=True)
    try:
        async with aiofiles.open(file_path, "wb") as out_file:
            while chunk := await file.read(1024):  # Чтение файла по частям (1024 байта за раз)
                await out_file.write(chunk)
        return file_path
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while saving the file: {str(e)}"
        )


def delete_file(file_path: str) -> None:
    if os.path.exists(file_path):
        os.remove(file_path)
