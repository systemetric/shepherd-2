"""Process an uploaded file"""
from argparse import FileType
import contextlib
import shutil
import tempfile
import fastapi
import zipfile
from pathlib import Path

from app.config import config
from app.runner import runner, States


def _is_python(file: fastapi.UploadFile) -> bool:
    return file.content_type.startswith("text") or file.filename.endswith(".py")


def _is_zip(file: fastapi.UploadFile) -> bool:
    return (("zip" in file.mimetype or file.filename.endswith(".zip")
             ) and zipfile.is_zipfile(file))


def _stage_python_file(dir: tempfile.TemporaryDirectory, in_file):
    entry_point = Path(dir.name) / config.usercode_entry_point
    with open(entry_point, 'wb') as out_file:
        content = in_file.file.read()
        out_file.write(content)


@contextlib.contextmanager
def _stage_usecode(file: fastapi.UploadFile):
    """Create the usecode directory with the file structure ready for the runner
    Raises FileType errors if unable to process usercode.
    """
    try:
        tempdir = tempfile.TemporaryDirectory()
        if _is_python(file):
            _stage_python_file(tempdir, file)
        elif _is_zip(file):
            pass  # TODO: zips
        else:
            raise FileType("Unknown File type, upload .zip or .py")

        yield tempdir
    finally:
        tempdir.cleanup()


def process_uploaded_file(file: fastapi.UploadFile):
    """Does the mime type and linter all return good?"""
    print("processing uploaded file")
    with _stage_usecode(file) as staging_dir:
        runner.state = States.STOPPED
        shutil.rmtree(config.usercode_path)
        shutil.move(staging_dir.name, config.usercode_path)
        runner.state = States.INIT
