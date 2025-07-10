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
