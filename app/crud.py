from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from .models import URLItem
from .utils import encode_base62

async def create_short_url(db: AsyncSession, original_url: str) -> URLItem:
    # Check if this URL is already shortened
    result = await db.execute(select(URLItem).where(URLItem.original_url == original_url))
    db_obj = result.scalars().first()
    if db_obj:
        return db_obj
    
    # Create new record
    db_obj = URLItem(original_url=original_url)
    db.add(db_obj)
    await db.flush() # Get the database-generated id
    
    # Generate base62 short_id using the internal DB id
    db_obj.short_id = encode_base62(db_obj.id)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def get_url_and_increment(db: AsyncSession, short_id: str) -> str | None:
    # Atomically increment using an F-expression and return original_url
    stmt = (
        update(URLItem)
        .where(URLItem.short_id == short_id)
        .values(clicks=URLItem.clicks + 1)
        .returning(URLItem.original_url)
    )
    result = await db.execute(stmt)
    original_url = result.scalar()
    if original_url:
        await db.commit()
    else:
        await db.rollback()
    return original_url

async def get_stats(db: AsyncSession, short_id: str) -> URLItem | None:
    result = await db.execute(select(URLItem).where(URLItem.short_id == short_id))
    return result.scalars().first()
