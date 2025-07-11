"""
Main project file to run fastapi microservice
"""
import uvicorn
from fastapi import FastAPI


app = FastAPI(docs_url="/docs")

@app.get("/get_logs")
async def get_logs() -> dict:
    """Returns logs info according to a query"""
    return { "message": "Here will be logs soon"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)
