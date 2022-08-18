import logging
from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse

import json
import os
import os.path as path
import re

from app.run import States
from app.run import runner
from app.config import config
import app.upload

_logger = logging.getLogger(__name__)

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

# ==============================================================================
# Files router
# ==============================================================================

files_router = APIRouter()


@files_router.get('/files')
def get_files():
    project_paths = [f for f in os.listdir(config.usr_src_path)
                     if path.isfile(path.join(config.usr_src_path, f))
                     and (f.endswith('.py') or f.endswith(".xml") or f == "blocks.json")
                     and f != 'main.py']

    def read_project(project_path: Path) -> dict:
        with open(config.usr_src_path / project_path, 'r') as project_file:
            content = project_file.read()
        return {
            'filename': project_path,
            'content': content
        }

    blocks = {}
    if path.exists(config.blocks_path):
        with open(config.blocks_path, 'r') as blocks_file:
            try:
                blocks = json.load(blocks_file)
            except ValueError:
                pass

    if "requires" not in blocks:
        blocks["requires"] = []
    if "header" not in blocks:
        blocks["header"] = ""
    if "footer" not in blocks:
        blocks["footer"] = ""
    if "blocks" not in blocks:
        blocks["blocks"] = []

    return {
        'main': config.usr_src_main_path.absolute(),
        'blocks': blocks,
        'projects': [read_project(p) for p in project_paths]
    }


@files_router.post("/save/{filename}")
def save_file(filename: str, body):
    _logger.debug(body)
    dots = len(re.findall("\\.", filename))
    if dots == 1:
        with open(path.join(config.usr_src_path, filename), 'w') as f:
            f.write(request.data.decode('utf-8'))
    else:
        _logger.warn("A file was attempted to be saved with too many dots: "
                     f"{filename}")
    return ""


@files_router.delete("/delete/<string:filename>")
def delete_file(filename):
    if filename == "blocks.json":
        return ""
    dots = len(re.findall("\\.", filename))
    if dots == 1:
        os.unlink(path.join(config.usr_src_path, filename))
    else:
        _logger.warn("A file was attempted to be saved with too many dots: "
                     f"{filename}")
    return ""
