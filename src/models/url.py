from datetime import datetime

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


from src.db.base import Base


class URL(Base):
    __tablename__ = 'urls'

    id : Mapped[int] = mapped_column(primary_key=True)
    original_url : Mapped[str] = mapped_column(String(255), index=True)
    short_url : Mapped[str] = mapped_column(String(255), index=True, unique=True, nullable=False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    click_count : Mapped[int] = mapped_column(default=0)

    def __repr__(self) -> str:
        return f"<URL(short_url='{self.short_url}', original_url='{self.original_url}')>"