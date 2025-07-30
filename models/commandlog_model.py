from datetime import datetime
from typing import Optional

from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class CommandLogModel(Base):
    """Commandlog model in a database"""
    __tablename__ = "commandlogs"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    function: Mapped[str]
    user_ip: Mapped[str]
    detail: Mapped[str]
    result: Mapped[str]
    reason: Mapped[Optional[str]]
    node_name: Mapped[str]
    log_time: Mapped[datetime]

    @staticmethod
    def from_log_file(csv_row: list, node_name: str):
        """Transforms a row from csv file to an object"""
        return CommandLogModel(
            username=csv_row[0],
            function=csv_row[1],
            user_ip=csv_row[4],
            detail=csv_row[5],
            result="Success" if csv_row[6] == "0" else "Failure",
            node_name=node_name,
            reason=csv_row[7],
            log_time=datetime.strptime(csv_row[9], '%Y-%m-%d %H:%M:%S')
        )

    __table_args__ = (
        Index("username_index", "username"),
        Index("commandlog_time_index", "log_time"),
    )
