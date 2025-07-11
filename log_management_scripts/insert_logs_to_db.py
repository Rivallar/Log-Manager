"""
Functions to transfer logs from log-files into a DB
"""
from sqlalchemy import create_engine, text

from database import async_session_factory
from log_setups import log_setups, LogType
from models.agentlog_model import AgentLogModel


correct_ORM_model = {
    "agentlogs": AgentLogModel
}


def extract_logs_from_log_file(db_data_table_name: str, unzipped_db_filename: str) -> list[tuple]:
    """Extracts log records from a given log file"""
    qry = f"SELECT * FROM {db_data_table_name}"
    engine = create_engine(f'sqlite:///{unzipped_db_filename}')
    with engine.connect() as conn:
        res = conn.execute(text(qry))
    return res.all()


async def insert_data(log_data: list[tuple], log_type: LogType) -> None:
    """Transforms given logs (db table rows) into correct ORM objects and sends them to log db"""
    async with async_session_factory() as session:
        logs_as_orm = [correct_ORM_model[log_type.value].from_log_file(item) for item in log_data]
        session.add_all(logs_as_orm)
        await session.commit()



async def insert_logs_to_db():
    """Transfers all logs from log files to appropriate tables in a database"""
    for setup in log_setups:
        logs_as_db_rows = extract_logs_from_log_file(setup.db_data_table_name, setup.unzipped_db_filename)
        await insert_data(logs_as_db_rows, setup.log_type)
