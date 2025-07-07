"""
Deletes old logs from logs folders and collects fresh logs from the servers.
"""

import logging
import os

from datetime import datetime, timedelta

import asyncssh

from config import settings

logger = logging.getLogger(__name__)


def delete_all_files_in_log_folders():
    """Delete all log files in all log folders."""
    logger.debug("Deleting all log files in all log folders.")
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), settings.PATH_TO_LOG_FOLDERS)
    for root, _dirs, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
                logger.debug(f"Deleted: {file_path}")
            except Exception as e:
                logger.error(f"Failed to delete {file_path}: {e}")
    logger.debug("Cleanup completed.")
    

async def get_fresh_logs():
    """Uploads fresh logs from a given servers"""
    logger.debug("Starting to collect fresh logs")
    curr_date = datetime.now()
    target_date = curr_date - timedelta(days=1)
    date_as_string = target_date.strftime("%Y-%m-%d")
    temp_remote_path = f"/home/logs/agentlogs/AgentLog_41_{date_as_string}_1.zip"
    temp_local_path = f"log_folders/agentlogs/AgentLog_41_{date_as_string}_1.zip"
    try:
        async with asyncssh.connect(settings.AGENTLOG_HOST, username=settings.AGENTLOG_USER, 
                            password=settings.AGENTLOG_PASSWORD, port=settings.SSH_PORT) as conn:
            async with conn.start_sftp_client() as sftp:
                await sftp.get(temp_remote_path, localpath=temp_local_path)
        logger.debug("Logs collected successfully")
    except Exception as e:
        logger.error(f"Failed to get logs: {e}")
