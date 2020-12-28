from fastapi import FastAPI
from pydantic import BaseSettings


class Settings(BaseSettings):
    output_file_path: str = "./logs.txt"
    usercode_path: str = "./files/"


settings = Settings()
