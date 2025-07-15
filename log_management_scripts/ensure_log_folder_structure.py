"""
A script to ensure correct log folder structure
"""
import logging
import os
from log_setups import log_setups

logger = logging.getLogger(__name__)


def check_folder_structure():
    """
    Ensures that all directories required by LogSetup.local_file_path exist.
    Creates missing directories as needed.
    """
    logger.info("Checking log folder structure")
    for setup in log_setups:
        dir_path = os.path.dirname(setup.local_file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            logger.info(f"Created missing directory: {dir_path}")
    logger.info("Log folder structure is ok.")


