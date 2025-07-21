"""
Deletes old logs from logs folders and collects fresh logs from the servers.
"""
import asyncio
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
            await sftp.mget(setup.remote_file_path, localpath=setup.local_file_path)


def unzip_and_cleanup(setup: LogSetup) -> None:
    """Unzips an uploaded log zipfile and deletes its archive"""
    with zipfile.ZipFile(setup.local_file_path, 'r') as zip_ref:
        zip_ref.getinfo(setup.archived_db_file_name).filename = setup.unzipped_db_filename
        zip_ref.extract(setup.archived_db_file_name)
    os.remove(setup.local_file_path)


def unzip_and_cleanup_commandlogs(setup: 'LogSetup') -> None:
    """Unzips an uploaded log zipfile and deletes its archive"""
    with zipfile.ZipFile(setup.local_file_path, 'r') as zip_ref:
        for info in zip_ref.infolist():
            if setup.db_data_table_name in info.filename:
                with zip_ref.open(info) as source, open(f"{setup.unzipped_csv_filename}", "wb") as target:
                    target.write(source.read())
                print(f"Extracted {info.filename} as commandlogs.csv")
                break
    os.remove(setup.local_file_path)


async def get_fresh_logs(log_setups: list[LogSetup]) -> None:
    """Uploads fresh logs from all sources"""
    logger.info("Starting to collect fresh logs")
    for setup in log_setups:
        with open(f"{setup.local_file_path}", "w") as dummy_file:
            pass
        try:
            await upload_log_file(setup=setup)
            logger.debug(f"Logs collected successfully for {setup.local_file_path}")
        except Exception as e:
            logger.error(f"Failed to get logs: {e}")
    logger.info("Logs collection task complete")


async def upload_log_file_v2(sftp, setup: LogSetup) -> None:
    """Upload single log file from remote host to appropriate local folder"""
    try:
        await sftp.mget(setup.remote_file_path, localpath=setup.local_file_path)
        logger.debug(f"Logs collected successfully for {setup.local_file_path}")
    except Exception as e:
        logger.error(f"Failed to get logs from {setup.remote_host}:{setup.remote_file_path}: {e}")


async def get_fresh_logs_from_one_server(log_setups: list[LogSetup]) -> None:
    """Uploads all fresh logs from a server (in case all logs are stored at one server)"""
    logger.info("Starting to collect fresh logs")
    async with asyncssh.connect(settings.AGENTLOG_USER, username=settings.AGENTLOG_PASSWORD,
                            password=settings.AGENTLOG_HOST, port=settings.SSH_PORT) as conn:
        async with conn.start_sftp_client() as sftp:
            tasks = []
            for setup in log_setups:
                with open(f"{setup.local_file_path}", "w") as dummy_file:
                        pass
                tasks.append(asyncio.create_task(upload_log_file_v2(sftp, setup)))
            await asyncio.gather(*tasks)
    logger.info("Logs collection task complete")

