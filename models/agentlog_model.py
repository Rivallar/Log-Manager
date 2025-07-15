import re

from datetime import datetime
from typing import Optional

from sqlalchemy import Index, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


def get_true_identities(imsi: Optional[str], msisdn: Optional[str]) -> tuple[int | None, int | None]:
    """Extracts imsi and msisdn as integer numbers from given string values"""
    true_imsi, true_msisdn = None, None

    if imsi:
        match_imsi = re.search(r'(25701\d{10})', imsi)
        true_imsi = int(match_imsi.group(1)) if match_imsi else None
        if not true_imsi:       # imsi field either blank or contains msisdn
            match_msisdn = re.search(r'(375\d{9})', imsi)
            true_msisdn = int(match_msisdn.group(1)) if match_msisdn else None
    if not true_msisdn and msisdn:
        match_msisdn = re.search(r'(375\d{9})', msisdn)
        true_msisdn = int(match_msisdn.group(1)) if match_msisdn else None
    return true_imsi, true_msisdn





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
    true_imsi: Mapped[Optional[int]] = mapped_column(BigInteger)
    true_msisdn: Mapped[Optional[int]] = mapped_column(BigInteger)
    data: Mapped[str]

    @staticmethod
    def from_log_file(db_row: tuple):
        """Transforms a row from logs database to an object"""
        start_command_index = db_row[16].find("MML:")
        command = db_row[16][start_command_index + len("MML:"):]
        true_imsi, true_msisdn = get_true_identities(imsi=db_row[3], msisdn=db_row[4])
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
            true_imsi=true_imsi,
            true_msisdn=true_msisdn,
            data=db_row[16],
        )

    __table_args__ = (
        Index("imsi_index", "true_imsi"),
        Index("msisdn_index", "true_msisdn"),
        Index("time_index", "log_time"),
    )
