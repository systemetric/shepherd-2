import shutil

from fastapi import APIRouter, HTTPException, UploadFile
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
    if runner.state != States.READY:
        raise HTTPException(status_code=409,
                            detail=f"Cannot start robot in state {runner.state}"
                            + ". Need to be in States.READY")
    runner.state = States.RUNNING


@runner_router.get("/state")
def get_state():
    return runner.current_state


@runner_router.get("/logs")
def output():
    return StreamingResponse(runner.get_output(), media_type="text/plain")

# ==============================================================================
# Upload router
# ==============================================================================


upload_router = APIRouter()


@upload_router.post("/upload")
def upload_file(file: UploadFile):
    app.upload.process_uploaded_file(file)
    return {
        "filename": file.filename,
        "filesize": len(file)
    }

