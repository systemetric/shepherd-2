from fastapi import FastAPI, Depends

from routers import runner

app = FastAPI()

app.include_router(runner.router)


@app.get("/", status_code=418)
def root():
    return {"description": "I'm a teapot"}
