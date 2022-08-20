from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from app.routers import runner_router, upload_router, files_router
from app.run import runner
from app.config import config
from app.upload import increase_max_file_size


app = FastAPI(
    title="Shepherd",
    version="0.0.1",
    docs_url="/api_docs",
    redoc_url="/api_redoc",
)

app.include_router(runner_router)
app.include_router(upload_router)
app.include_router(files_router)

app.mount("/editor", StaticFiles(directory=config.editor_path, html=True), name="editor")
app.mount("/docs", StaticFiles(directory=config.docs_path, html=True), name="docs")


@app.on_event("startup")
def startup_event():
    increase_max_file_size()


@app.on_event("shutdown")
def shutdown_event():
    """Kill any running usercode"""
    runner.shutdown()
    os.remove(config.usr_fifo_path)


@app.get("/")
def root():
    return "Root of shepherd-2"


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
