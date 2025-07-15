"""
Main project file to run fastapi microservice
"""
import uvicorn
from fastapi import FastAPI

from api.query_routes import router as query_logs_router


app = FastAPI(docs_url="/docs")
app.include_router(query_logs_router)


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
