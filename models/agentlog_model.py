from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class AgentLogModel(Base):
    """Agentlog model in a database"""
    __tablename__ = "agentlogs"

    id: Mapped[int] = mapped_column(primary_key=True)
    cmd_code: Mapped[str]
    user_type: Mapped[int]
    imsi: Mapped[Optional[str]]
    msisdn: Mapped[Optional[str]]
    log_time: Mapped[datetime]
    operator: Mapped[str]
    agent_type: Mapped[int]
    node_ip: Mapped[str]
    command: Mapped[str]
    if_error: Mapped[bool]
    data: Mapped[str]

    @staticmethod
    def from_log_file(db_row: tuple):
        """Transforms a row from logs database to an object"""
        start_command_index = db_row[16].find("MML:")
        command = db_row[16][start_command_index + len("MML:"):]
        return AgentLogModel(
            cmd_code=db_row[1],
            user_type=db_row[2],
            imsi=db_row[3],
            msisdn=db_row[4],
            log_time=datetime.strptime(db_row[6], '%Y-%m-%d %H:%M:%S'),
            operator=db_row[7],
            agent_type=db_row[8],
            node_ip=db_row[10],
            command=command,
            if_error=bool(db_row[14]),
            data=db_row[16],
        )

