import re
from datetime import datetime
from typing import Optional

from sqlalchemy import Index, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class SoapLogModel(Base):
    """Soaplog model in a database"""
    __tablename__ = "soaplogs"

    id: Mapped[int] = mapped_column(primary_key=True)
    log_time: Mapped[datetime]
    cmd_code: Mapped[str]
    user_id: Mapped[str]
    request: Mapped[str]
    if_error: Mapped[bool]
    error_description: Mapped[Optional[str]]
    node_name: Mapped[str]
    true_msisdn: Mapped[Optional[int]] = mapped_column(BigInteger)

    @staticmethod
    def get_request_body(full_request: str) -> str:
        """Extracts body from a full request"""
        starter = '<SOAP-ENV:Body>'
        finisher = '</SOAP-ENV:Body>'
        start_ind = full_request.find(starter) + len(starter)
        end_ind = full_request.find(finisher)
        return full_request[start_ind:end_ind].strip()

    @staticmethod
    def from_log_file(db_row: tuple, node_name: str):
        """Transforms a row from logs database to an object"""
        match_msisdn = re.search(r'(375\d{9})', db_row[5])
        return SoapLogModel(
            log_time=datetime.strptime(db_row[1], '%Y-%m-%d %H:%M:%S:%f'),
            cmd_code=db_row[3],
            user_id=db_row[5],
            request=SoapLogModel.get_request_body(db_row[6]),
            if_error=bool(db_row[8]),
            error_description=db_row[9] if db_row[8] else None,
            node_name=node_name,
            true_msisdn = int(match_msisdn.group(1)) if match_msisdn else None
        )

    __table_args__ = (
        Index("soaplog_time_index", "log_time"),
        Index("soap_msisdn_index", "true_msisdn")
    )
