"""
This file contains information about what logs to collect, where to find them and where to keep them locally
"""
import enum
from datetime import datetime, timedelta
from typing import Optional

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
    node_name: str
    remote_host: str
    username: str
    password: str
    remote_file_path: str
    local_file_path: str
    log_pointer: Optional[str] = None       # may be db table name or filename in an archive

    @property
    def unzipped_db_filename(self) -> str:
        """Returns a name of an unzipped database file"""
        return self.local_file_path.replace(".zip", ".db")

    @property
    def unzipped_csv_filename(self) -> str:
        """Returns a name of an unzipped database file"""
        return self.local_file_path.replace(".zip", ".csv")

    @property
    def archived_db_file_name(self) -> str:
        """Returns a name of a sqlite file inside an archive"""
        return f"sqlite_diary_data_{formatted_yesterday_date.replace('-', '')}.db"


log_setups = []

USPP41 = LogSetup(
    log_type=LogType.AGENTLOGS,
    node_name="USPP41",
    remote_host=settings.AGENTLOG_HOST,
    username=settings.AGENTLOG_USER,
    password=settings.AGENTLOG_PASSWORD,
    remote_file_path=f"/home/logs/agentlogs/AgentLog_41_{formatted_yesterday_date}_1.zip",
    local_file_path=f"{settings.PATH_TO_LOG_FOLDERS}/{LogType.AGENTLOGS.value}/AgentLog_41.zip",
    log_pointer="D_HISTORYLOG"
)
log_setups.append(USPP41)

USPP42 = LogSetup(
    log_type=LogType.AGENTLOGS,
    node_name="USPP42",
    remote_host=settings.AGENTLOG_HOST,
    username=settings.AGENTLOG_USER,
    password=settings.AGENTLOG_PASSWORD,
    remote_file_path=f"/home/logs/agentlogs/AgentLog_42_{formatted_yesterday_date}_1.zip",
    local_file_path=f"{settings.PATH_TO_LOG_FOLDERS}/{LogType.AGENTLOGS.value}/AgentLog_42.zip",
    log_pointer="D_HISTORYLOG"
)
log_setups.append(USPP42)

ASBC144 = LogSetup(
    log_type=LogType.COMMANDLOGS,
    node_name="ASBC144",
    remote_host=settings.AGENTLOG_HOST,
    username=settings.AGENTLOG_USER,
    password=settings.AGENTLOG_PASSWORD,
    remote_file_path=f"/home/logs/ommarc/{formatted_yesterday_date.split('-')[0]}/sbc/asbc144/{formatted_yesterday_date}_1.zip",
    local_file_path=f"{settings.PATH_TO_LOG_FOLDERS}/{LogType.COMMANDLOGS.value}/ASBC144/logs.zip",
    log_pointer="operation_log"
)
log_setups.append(ASBC144)


SSS113 = LogSetup(
    log_type=LogType.SOAPLOGS,
    node_name="SSS113",
    remote_host=settings.AGENTLOG_HOST,
    username=settings.AGENTLOG_USER,
    password=settings.AGENTLOG_PASSWORD,
    remote_file_path=f"/home/logs/soap/sss/sss113/{datetime.now().strftime('%Y%m%d')}_sspi_soap_log_bak.sl3",
    local_file_path=f"{settings.PATH_TO_LOG_FOLDERS}/{LogType.SOAPLOGS.value}/SSS113/soaplogs.sl3",
    log_pointer="soap_log"
)
log_setups.append(SSS113)


AGCF121 = LogSetup(
    log_type=LogType.SOAPLOGS,
    node_name="AGCF121",
    remote_host=settings.AGENTLOG_HOST,
    username=settings.AGENTLOG_USER,
    password=settings.AGENTLOG_PASSWORD,
    remote_file_path=f"/home/logs/soap/agcf/agcf121/SoapLog_{datetime.now().strftime('%Y%m%d')}0500.csv",
    local_file_path=f"{settings.PATH_TO_LOG_FOLDERS}/{LogType.SOAPLOGS.value}/AGCF121/soaplogs.csv",
    log_pointer="soap_log"
)
log_setups.append(AGCF121)

commandlog_nodes = [setup.node_name for setup in log_setups if setup.log_type == LogType.COMMANDLOGS]
