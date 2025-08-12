"""
Main project file to run fastapi microservice
"""
from contextlib import asynccontextmanager
import logging
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.query_routes import router as query_logs_router
from api.service_routes import router as service_router
from config import settings
from log_management_scripts.collect_logs_and_cleanup import get_fresh_logs_from_one_server, unzip_and_cleanup
from log_management_scripts.ensure_log_folder_structure import check_folder_structure
from log_management_scripts.insert_logs_to_db import insert_logs_to_db
from log_setups import log_setups
from web_routes import router as web_routes_router


logging.basicConfig(level=settings.LOGGING_LEVEL)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Starts scheduled tasks and preparation scripts"""
    # check_folder_structure()
    # await get_fresh_logs_from_one_server([log_setups[3]])
    # for log_setup in log_setups:
    #     unzip_and_cleanup(log_setup)
    # await insert_logs_to_db()
    yield


app = FastAPI(docs_url="/docs", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(web_routes_router)
app.include_router(query_logs_router, prefix="/api")
if settings.SERVICE_ROUTES_NEEDED:
    app.include_router(service_router, prefix="/api")

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)
