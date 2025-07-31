"""
SoapLog schemas
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SoapLogSchema(BaseModel):
    """Soaplog record as an object for API"""
    log_time: datetime
    cmd_code: str
    user_id: str
    request: str
    if_error: bool
    error_description: Optional[str]
    node_name: str