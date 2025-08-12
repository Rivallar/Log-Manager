from log_setups import log_setups
from .insert_logs_to_db import insert_logs_to_db
from .collect_logs_and_cleanup import get_fresh_logs_from_one_server, unzip_and_cleanup, \
    delete_all_files_in_log_folders, delete_old_logs


async def update_db_with_fresh_logs() -> None:
    """This function is an aggregation of all scripts to collect new logs"""
    try:
        await delete_old_logs()
        await get_fresh_logs_from_one_server(log_setups)
        for log_setup in log_setups:
            unzip_and_cleanup(log_setup)
        await insert_logs_to_db()
    finally:
        delete_all_files_in_log_folders()
