from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Parent class to all database models"""

    def __repr__(self):
        cols = []
        for col in self.__table__.columns.keys():
            cols.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.__name__} {' '.join(cols)}>"
