from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class LinkModel(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(8), unique=True, nullable=False, index=True)
    original_url = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime, nullable=True)
    click_count = Column(Integer, default=0)
    last_accessed = Column(DateTime, nullable=True)
