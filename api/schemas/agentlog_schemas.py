"""
AgentLog schemas
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AgentLogSchema(BaseModel):
    """Agentlog record as an object for API"""
    cmd_code: str
    imsi: Optional[str]
    msisdn: Optional[str]
    log_time: datetime
    operator: str
    agent_type: int
    node_ip: str
    command: str
    if_error: bool
