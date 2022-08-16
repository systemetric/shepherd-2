from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse

from app.runner import States
from app.runner import runner
import app.upload

# ==============================================================================
# Runner router
# ==============================================================================

runner_router = APIRouter()


@runner_router.get("/stop")
def stop():
    runner.state = States.STOPPED


@runner_router.get("/start")
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


upload_router = APIRouter()

@upload_router.post("/upload", status_code=201)
def upload_file(file: UploadFile = File(...)):
    print("file upload triggered")
    app.upload.process_uploaded_file(file)
    return {
        "filename": file.filename,
    }

