from app.settings import Settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

engine = create_async_engine(url=Settings().DATABASE_URL, echo=True, future=True, pool_pre_ping=True)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autocommit=False,
    expire_on_commit=False
)


async def get_db_session() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        yield session
