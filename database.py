"""
Main tools to work with database
"""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config import settings


async_engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=False,
)
async_session_factory = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    """Parent class to all database models"""

    def __repr__(self):
        cols = []
        for col in self.__table__.columns.keys():
            cols.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.__name__} {' '.join(cols)}>"
