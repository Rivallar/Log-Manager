import asyncio
from log_management_scripts.insert_logs_to_db import insert_data, extract_sql_logs, extract_csv_logs
from log_setups import log_setups

setup = log_setups[2]
raw_logs = extract_csv_logs(setup.unzipped_csv_filename)
asyncio.run(insert_data(raw_logs, setup.log_type, setup.node_name))