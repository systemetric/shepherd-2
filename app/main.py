from fastapi import FastAPI
import uvicorn

from app import routers
from app.runner import runner

app = FastAPI(
    title="Shepherd",
    version="0.0.1",
    docs_url="/api_docs",
    redoc_url="/api_redoc",
)

app.include_router(routers.runner_router)
app.include_router(routers.upload_router)

@app.get("/")
def root():
    return "Root of shepherd-2"

@app.on_event("shutdown")
def shutdown_event():
    """Make sure that we kill any running usercode
    Might not work if we crash or die
    """
    runner.stop()


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')