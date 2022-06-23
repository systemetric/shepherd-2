from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.runner import RunnerHandler, RunnerState

handler = RunnerHandler()

router = APIRouter()

@router.get("/stop")
def stop():
    handler.state = RunnerState.STOPPED

@router.get("/start")
def start():
    handler.state = RunnerState.RUNNING

@router.post("/state")
def set_state(new_state: RunnerState):
    handler.state = new_state
    return handler.state

@router.get("/state")
def get_state():
    return handler.state

@router.get("/logs")
async def output():
    return StreamingResponse(handler.get_output(), media_type="text/plain")
