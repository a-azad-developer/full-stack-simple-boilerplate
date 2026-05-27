from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings

engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI))


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        yield session


AsyncSessionLocal = AsyncSession
