import os
import sys
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import get_settings

# Debug: Print raw environment variable BEFORE any processing
raw_db_url = os.getenv("DATABASE_URL", "NOT_SET")
print(f"DEBUG: Raw DATABASE_URL from env: {raw_db_url[:60]}...", file=sys.stderr, flush=True)

settings = get_settings()

# Debug: Print after pydantic processing
print(f"DEBUG: After pydantic: {settings.database_url[:60]}...", file=sys.stderr, flush=True)

# Transform DATABASE_URL for asyncpg driver compatibility
# Railway provides postgresql:// URLs, but SQLAlchemy with asyncpg needs postgresql+asyncpg://
database_url = settings.database_url
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    print(f"DEBUG: After transform: {database_url[:60]}...", file=sys.stderr, flush=True)

engine = create_async_engine(
    database_url,
    echo=False,
    pool_size=20,
    max_overflow=10,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
