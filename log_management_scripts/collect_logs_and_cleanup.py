"""
Deletes old logs from logs folders and collects fresh logs from the servers.
"""

import logging
import os
import zipfile

import asyncssh

from config import settings
from log_setups import LogSetup

logger = logging.getLogger(__name__)


def delete_all_files_in_log_folders() -> None:
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


async def upload_log_file(setup: LogSetup) -> None:
    """Upload single log file from remote host to appropriate local folder"""
    async with asyncssh.connect(setup.remote_host, username=setup.username,
                            password=setup.password, port=settings.SSH_PORT) as conn:
        async with conn.start_sftp_client() as sftp:
            await sftp.get(setup.remote_file_path, localpath=setup.local_file_path)


def unzip_and_cleanup(setup: LogSetup) -> None:
    """Unzips an uploaded log zipfile and deletes its archive"""
    with zipfile.ZipFile(setup.local_file_path, 'r') as zip_ref:
        zip_ref.getinfo(setup.archived_db_file_name).filename = setup.unzipped_db_filename
        zip_ref.extract(setup.archived_db_file_name)
    os.remove(setup.local_file_path)


async def get_fresh_logs(log_setups: list[LogSetup]) -> None:
    """Uploads fresh logs from all sources"""
    logger.info("Starting to collect fresh logs")
    for setup in log_setups:
        try:
            await upload_log_file(setup=setup)
            logger.debug(f"Logs collected successfully for {setup.local_file_path}")
        except Exception as e:
            logger.error(f"Failed to get logs: {e}")
    logger.info("Logs collection task complete")

