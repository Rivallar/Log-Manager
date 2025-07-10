from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AgentLogSchema(BaseModel):
    """DB schema for agentlog"""
    cmd_code: str
    user_type: int
    imsi: Optional[str]
    msisdn: Optional[str]
    log_time: datetime
    operator: str
    agent_type: int
    node_ip: str
    command: str
    if_error: bool
    data: str

    @staticmethod
    def from_log_file(db_row: tuple):
        """Transforms a row from logs database to an object"""
        start_command_index = db_row[16].find("MML:")
        command = db_row[16][start_command_index + len("MML:"):]
        return AgentLogSchema(
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
