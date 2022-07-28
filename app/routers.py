from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.runner import States
from app.runner import runner

router = APIRouter()

@router.get("/stop")
def stop():
    runner.state = States.STOPPED

@router.get("/start")
def start():
    if runner.state != States.READY:
        raise HTTPException(status_code=409,
                            detail=f"Cannot start robot in state {runner.state}"
                            + ". Need to be in States.READY")
    runner.state = States.RUNNING

@router.get("/state")
def get_state():
    return runner.current_state

@router.get("/logs")
async def output():
    return StreamingResponse(runner.get_output(), media_type="text/plain")
