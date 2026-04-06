from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String
from .database import Base

class URLItem(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    short_id: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=True)
    original_url: Mapped[str] = mapped_column(String, unique=True, index=True)
    clicks: Mapped[int] = mapped_column(Integer, default=0)
