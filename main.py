import logging
from log_management_scripts.collect_logs_and_cleanup import delete_all_files_in_log_folders

from config import settings

logging.basicConfig(level=settings.LOGGING_LEVEL)

delete_all_files_in_log_folders()
