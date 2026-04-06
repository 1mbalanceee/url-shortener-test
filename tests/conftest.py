import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.database import engine, Base
from app.main import app

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    # проверка чистая ли база данных
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
