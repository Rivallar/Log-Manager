"""
Functions to transfer logs from log-files into a DB
"""
import csv
import logging
from sqlalchemy import create_engine, text

from database import async_session_factory
from log_setups import log_setups, LogType
from models.agentlog_model import AgentLogModel
from models.commandlog_model import CommandLogModel
from models.soaplog_model import SoapLogModel

logger = logging.getLogger(__name__)

correct_ORM_model = {
    "agentlogs": AgentLogModel,
    "commandlogs": CommandLogModel,
    "soaplogs": SoapLogModel
}


def extract_sql_logs(db_data_table_name: str, db_filename: str) -> list[tuple]:
    """Extracts log records from a given log file"""
    qry = f"SELECT * FROM {db_data_table_name}"
    engine = create_engine(f'sqlite:///{db_filename}')
    with engine.connect() as conn:
        res = conn.execute(text(qry))
    return res.all()


def extract_csv_logs(csv_file_path: str) -> list[list]:
    """Extracts commandlog records from a given log file"""
    with open(csv_file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        _header = next(csv_reader, None)
        return list(csv_reader)


async def insert_data(log_data: list[tuple], log_type: LogType, node_name: str) -> None:
    """Transforms given logs (db table rows) into correct ORM objects and sends them to log db"""
    async with async_session_factory() as session:
        logs_as_orm = [correct_ORM_model[log_type.value].from_log_file(item, node_name) for item in log_data]
        session.add_all(logs_as_orm)
        await session.commit()



async def insert_logs_to_db():
    """Transfers all logs from log files to appropriate tables in a database"""
    logger.info("LOG TRANSFER TASK STARTED")
    for setup in log_setups:
        match setup.log_type:
            case LogType.AGENTLOGS:
                raw_logs = extract_sql_logs(setup.log_pointer, setup.unzipped_db_filename)
            case LogType.COMMANDLOGS:
                raw_logs = extract_csv_logs(setup.unzipped_csv_filename)
            case LogType.SOAPLOGS:
                raw_logs = extract_sql_logs(setup.log_pointer, setup.local_file_path)

        await insert_data(raw_logs, setup.log_type, setup.node_name)
        logger.info(f"Collected {len(raw_logs)} records from {setup.local_file_path}")
    logger.info("LOG TRANSFER TASK FINISHED")
