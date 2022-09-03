import os

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import config
from app.logging import configure_logging, logger
from app.routers import files_router, runner_router, upload_router
from app.run import runner
from app.upload import increase_max_file_size

configure_logging()


shepherd = FastAPI(
    title="Shepherd",
    version="0.0.1",
    docs_url="/api_docs",
    redoc_url="/api_redoc",
    debug=True,
)

shepherd.include_router(runner_router)
shepherd.include_router(upload_router)
shepherd.include_router(files_router)

shepherd.mount("/editor", StaticFiles(directory=config.editor_path, html=True), name="editor")
shepherd.mount("/docs", StaticFiles(directory=config.docs_path, html=True), name="docs")
shepherd.mount("/static", StaticFiles(directory=config.static_path, html=True), name="static")


@shepherd.on_event("startup")
def startup_event():
    """Setup which is run before the rest of shepherd.
    This works a round bugs in python. See doc string of `increase_max_file_size`
    """
    increase_max_file_size()


@shepherd.on_event("shutdown")
def shutdown_event():
    """Kill any running usercode"""
    logger.info("Shutting down usercode forcing may leave usercode still running")
    runner.shutdown()
    if os.path.exists(config.usr_in_path) is True:
        os.remove(config.usr_in_path)


@shepherd.get("/")
def root():
    return "Root of shepherd-2"


if __name__ == '__main__':
    uvicorn.run(shepherd, port=8080, host='0.0.0.0')
