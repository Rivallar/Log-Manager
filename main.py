"""
Main project file to run fastapi microservice
"""
from contextlib import asynccontextmanager
import logging
import uvicorn
from fastapi import FastAPI

from api.query_routes import router as query_logs_router
from config import settings
from log_management_scripts.ensure_log_folder_structure import check_folder_structure


logging.basicConfig(level=settings.LOGGING_LEVEL)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Starts scheduled tasks and preparation scripts"""
    check_folder_structure()
    yield



app = FastAPI(docs_url="/docs", lifespan=lifespan)
app.include_router(query_logs_router)


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
