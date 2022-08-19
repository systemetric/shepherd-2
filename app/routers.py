import logging
from fastapi import APIRouter, HTTPException, UploadFile, File, Request
from pydantic import BaseModel

from app.run import States
from app.run import runner
import app.editor
import app.upload

_logger = logging.getLogger(__name__)

# ==============================================================================
# Runner router
# ==============================================================================

runner_router = APIRouter(prefix="/run")


@runner_router.post("/stop")
def stop():
    runner.state = States.STOPPED


@runner_router.post("/start")
def start():
    """Start the robot, really the check and the start should be in a lock"""
    # TODO: https://github.com/systemetric/shepherd-2/issues/18
    if runner.state != States.INIT:
        raise HTTPException(status_code=409,
                            detail=f"Cannot start robot in state {runner.state}"
                            + ". Need to be in States.INIT")
    # runner.state = States.RUNNING
    type(runner).state.__set__(runner, States.RUNNING)


@runner_router.get("/state")
def get_state():
    return runner.state


@runner_router.get("/logs")
def output():
    return runner.get_output()

# ==============================================================================
# Upload router
# ==============================================================================


upload_router = APIRouter(prefix="/upload")

@upload_router.post("/upload", status_code=201)
def upload_file(uploaded_file: UploadFile = File(...)):
    _logger.info("File uploaded to staging")
    app.upload.process_uploaded_file(uploaded_file)
    return {
        "filename": uploaded_file.filename,
    }

# ==============================================================================
# Files router
# ==============================================================================

files_router = APIRouter(prefix="/files")

class SheepFile(BaseModel):
    contents: str


@files_router.get('/')
def get_files():
    return app.editor.get_files()


@files_router.post("/save/{filename}")
async def save_file(filename: str, request: Request):
    app.editor.save_file(filename, await request.body())


@files_router.delete("/delete/{filename}")
def delete_file(filename: str):
    app.editor.delete_file(filename)
