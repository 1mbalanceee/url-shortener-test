from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .database import engine, Base, get_db
from . import schemas, crud

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB schema on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(title="URL Shortener API", lifespan=lifespan)

@app.post("/shorten", response_model=schemas.ShortenResponse)
async def shorten_url(request: schemas.ShortenRequest, db: AsyncSession = Depends(get_db)):
    # Convert Pydantic AnyUrl to string safely
    url_str = str(request.url)
    url_item = await crud.create_short_url(db, url_str)
    return schemas.ShortenResponse(short_id=url_item.short_id)

@app.get("/{short_id}")
async def redirect_url(short_id: str, db: AsyncSession = Depends(get_db)):
    original_url = await crud.get_url_and_increment(db, short_id)
    if not original_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return RedirectResponse(url=original_url, status_code=302)

@app.get("/stats/{short_id}", response_model=schemas.StatsResponse)
async def get_stats(short_id: str, db: AsyncSession = Depends(get_db)):
    stats = await crud.get_stats(db, short_id)
    if not stats:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return stats
