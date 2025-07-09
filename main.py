import logging
from log_management_scripts.collect_logs_and_cleanup import delete_all_files_in_log_folders, unzip_and_cleanup

from config import settings
from log_setups import log_setups, LogSetup

logging.basicConfig(level=settings.LOGGING_LEVEL)

# delete_all_files_in_log_folders()
for setup in log_setups:
    unzip_and_cleanup(setup=setup)
