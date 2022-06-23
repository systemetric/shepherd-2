from fastapi import FastAPI

from app import routers

app = FastAPI()

app.include_router(routers.router)


@app.get("/")
def root():
    return "Root of shepherd-2"
