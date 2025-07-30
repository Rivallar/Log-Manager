"""
Commandlog schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class CommandLogSchema(BaseModel):
    """Commandlog record as an object for API"""
    username: str
    log_time: datetime
    detail: str
    result: str
    reason: Optional[str] = None
    function: str
    user_ip: str
    node_name: str
