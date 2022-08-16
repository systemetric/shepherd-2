from fastapi import FastAPI
import uvicorn

from app import routers
from app.runner import runner

def increase_max_file_size():
    """This is the maximum filesize which can be uploaded to shepherd.
    see app.upload._fix_bad_zips for more info.

    starlette which FastAPI uses does not allow for us to set the spool_max_size
    in the constructor instead defining it as a class attribute so we override
    this class attribute
    """
    from starlette.datastructures import UploadFile as StarletteUploadFile
    # the original size * a big number
    StarletteUploadFile.spool_max_size = (1024 * 1024) * 99999999999999999


# Call before any chance of any UploadFiles being created
increase_max_file_size()

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
    runner.shutdown()


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')