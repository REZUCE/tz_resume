from pydantic_settings import BaseSettings


class WorkFile(BaseSettings):
    CHUNK_SIZE: int = 1024 * 1024
    FILES_PATH: str = "app/static/files/"


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "postgres"
    DB_DRIVER: str = "postgresql+asyncpg"



    @property
    def DATABASE_URL(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_prefix = ".env"
