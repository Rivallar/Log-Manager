"""
Functions to transfer logs from log-files into a DB
"""
import csv
from datetime import datetime, date, timedelta
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


def extract_csv_logs(csv_file_path: str, agcf=False) -> list[list]:
    """Extracts commandlog records from a given log file"""
    with open(csv_file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        _header = next(csv_reader, None)
        if not agcf:
            return list(csv_reader)
        else:
            target_date = date.today() - timedelta(days=2)  # full logs only 2 days ago or later
            logs = []
            for row in csv_reader:
                try:
                    log_datetime = datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')
                except (ValueError, IndexError):
                    print("Error!")
                    continue
                if log_datetime.date() == target_date:
                    logs.append(row)
            return logs


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
        try:
            match setup.log_type:
                case LogType.AGENTLOGS:
                    raw_logs = extract_sql_logs(setup.log_pointer, setup.unzipped_db_filename)
                case LogType.COMMANDLOGS:
                    raw_logs = extract_csv_logs(setup.unzipped_csv_filename)
                case LogType.SOAPLOGS:
                    if "SSS" in setup.node_name:
                        raw_logs = extract_sql_logs(setup.log_pointer, setup.local_file_path)
                    else:
                        raw_logs = extract_csv_logs(setup.local_file_path, agcf=True)
        except FileNotFoundError:
            logger.error(
                f"Unable to insert logs to db: unzipped log file for {setup.node_name} was not found. Skipping"
            )
            continue

        await insert_data(raw_logs, setup.log_type, setup.node_name)
        logger.info(f"Collected {len(raw_logs)} records from {setup.local_file_path}")
    logger.info("LOG TRANSFER TASK FINISHED")
