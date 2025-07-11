"""
This file contains information about what logs to collect, where to find them and where to keep them locally
"""
import enum
from datetime import datetime, timedelta

from pydantic import BaseModel

from config import settings


formatted_yesterday_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")



class LogType(enum.Enum):
    """The type of log files"""
    AGENTLOGS = "agentlogs"
    COMMANDLOGS = "commandlogs"
    SOAPLOGS = "soaplogs"


class LogSetup(BaseModel):
    """A class to represent all info about how to process a certain log"""
    log_type: LogType
    remote_host: str
    username: str
    password: str
    remote_file_path: str
    local_file_path: str
    archived_db_file_name: str = f"sqlite_diary_data_{formatted_yesterday_date.replace('-', '')}.db"
    db_data_table_name: str

    @property
    def unzipped_db_filename(self) -> str:
        """Returns a name of an unzipped database file"""
        return self.local_file_path.replace(".zip", ".db")


log_setups = []

USPP41 = LogSetup(
    log_type=LogType.AGENTLOGS,
    remote_host=settings.AGENTLOG_HOST,
    username=settings.AGENTLOG_USER,
    password=settings.AGENTLOG_PASSWORD,
    remote_file_path=f"/home/logs/agentlogs/AgentLog_41_{formatted_yesterday_date}_1.zip",
    local_file_path=f"{settings.PATH_TO_LOG_FOLDERS}/{LogType.AGENTLOGS.value}/AgentLog_41.zip",
    db_data_table_name="D_HISTORYLOG"
)
log_setups.append(USPP41)

USPP42 = LogSetup(
    log_type=LogType.AGENTLOGS,
    remote_host=settings.AGENTLOG_HOST,
    username=settings.AGENTLOG_USER,
    password=settings.AGENTLOG_PASSWORD,
    remote_file_path=f"/home/logs/agentlogs/AgentLog_42_{formatted_yesterday_date}_1.zip",
    local_file_path=f"{settings.PATH_TO_LOG_FOLDERS}/{LogType.AGENTLOGS.value}/AgentLog_42.zip",
    db_data_table_name="D_HISTORYLOG"
)
log_setups.append(USPP42)
