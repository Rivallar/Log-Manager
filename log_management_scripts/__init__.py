from asyncio import sleep
from datetime import datetime, timedelta
import logging

from config import settings
from log_setups import log_setups
from .insert_logs_to_db import insert_logs_to_db
from .collect_logs_and_cleanup import get_fresh_logs_from_one_server, unzip_and_cleanup, \
    delete_all_files_in_log_folders, delete_old_logs


logger = logging.getLogger(__name__)

async def update_db_with_fresh_logs() -> None:
    """This function is an aggregation of all scripts to collect new logs"""
    try:
        await delete_old_logs()
        await get_fresh_logs_from_one_server(log_setups)
        for log_setup in log_setups:
            unzip_and_cleanup(log_setup)
        await insert_logs_to_db()
    except TimeoutError as e:
        logger.error(f"Failed to connect to server {settings.AGENTLOG_HOST}: {e}")
    finally:
        delete_all_files_in_log_folders()


async def update_logs_by_schedule() -> None:
    """Daily task to manage fresh and old logs"""
    logger.info("Daily task to collect logs started")
    while True:
        curr_time = datetime.now()
        hour, minute = settings.SCHEDULED_TIME
        target_time = curr_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if curr_time > target_time:
            target_time += timedelta(days=1)
        time_to_wait = (target_time - curr_time).total_seconds()
        logger.info(f"Daily task to collect logs gonna sleep till {target_time}")
        await sleep(time_to_wait)
        await update_db_with_fresh_logs()