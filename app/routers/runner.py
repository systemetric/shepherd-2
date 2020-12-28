from fastapi import APIRouter
from fastapi.responses import FileResponse, StreamingResponse

from dependencies import RunnerHandler

handler = RunnerHandler()

router = APIRouter(prefix="/runner")

@router.post("/start", status_code=201)
def start():
    handler.start_user_code()

@router.post("/stop")
def stop():
    handler.stop_user_code()

@router.get("/state")
def state():
    return handler.get_state()

@router.get("/output")
async def output():
    return StreamingResponse(handler.get_output(), media_type="text/plain")