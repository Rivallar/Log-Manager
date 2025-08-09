"""
Deletes old logs from logs folders and collects fresh logs from the servers.
"""
import asyncio
import logging
import os
import zipfile

import asyncssh

from config import settings
from log_setups import LogSetup, LogType

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


def unzip_apentlog(setup: LogSetup) -> None:
    """Unzips an archive of agentlogs"""
    with zipfile.ZipFile(setup.local_file_path, 'r') as zip_ref:
        zip_ref.getinfo(setup.archived_db_file_name).filename = setup.unzipped_db_filename
        zip_ref.extract(setup.archived_db_file_name)


def unzip_commandlog(setup: LogSetup) -> None:
    """Unzips an archive of commandlogs"""
    with zipfile.ZipFile(setup.local_file_path, 'r') as zip_ref:
        for info in zip_ref.infolist():
            if setup.log_pointer in info.filename:
                with zip_ref.open(info) as source, open(f"{setup.unzipped_csv_filename}", "wb") as target:
                    target.write(source.read())
                break


def unzip_and_cleanup(setup: LogSetup) -> None:
    """Unzips an uploaded log zipfile and deletes its archive"""
    try:
        match setup.log_type:
            case LogType.AGENTLOGS:
                unzip_apentlog(setup)
            case LogType.COMMANDLOGS:
                unzip_commandlog(setup)
            case LogType.SOAPLOGS:
                return
        os.remove(setup.local_file_path)
    except FileNotFoundError:
        logger.error(f"Unable to unzip/delete {setup.local_file_path}. File not found.Skipping.")



async def upload_log_file(sftp, setup: LogSetup) -> None:
    """Upload single log file from remote host to appropriate local folder"""
    try:
        await sftp.mget(setup.remote_file_path, localpath=setup.local_file_path)
        logger.debug(f"Logs collected successfully for {setup.local_file_path}")
    except Exception as e:
        logger.error(f"Failed to get logs from {setup.remote_host}:{setup.remote_file_path}: {e}")


async def get_fresh_logs_from_one_server(log_setups: list[LogSetup]) -> None:
    """Uploads all fresh logs from a server (in case all logs are stored at one server)"""
    logger.info("Starting to collect fresh logs")
    async with asyncssh.connect(settings.AGENTLOG_HOST, username=settings.AGENTLOG_USER,
                                password=settings.AGENTLOG_PASSWORD, port=settings.SSH_PORT,
                                known_hosts=None) as conn:
        async with conn.start_sftp_client() as sftp:
            tasks = []
            for setup in log_setups:
                with open(f"{setup.local_file_path}", "w") as _dummy_file:
                    pass
                tasks.append(asyncio.create_task(upload_log_file(sftp, setup)))
            await asyncio.gather(*tasks)
    logger.info("Logs collection task complete")
