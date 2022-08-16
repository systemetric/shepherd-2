"""Process an uploaded file"""
import contextlib
import shutil
import tempfile
import fastapi
import types
import zipfile
from pathlib import Path

from app.config import config
from app.runner import runner, States


def _is_python(file: fastapi.UploadFile) -> bool:
    return file.content_type.startswith("text") or file.filename.endswith(".py")


def _is_zip(file: fastapi.UploadFile) -> bool:
    return (("zip" in file.content_type) or file.filename.endswith(".zip"))


def _stage_python(dir: tempfile.TemporaryDirectory, in_file: fastapi.UploadFile):
    entry_point = Path(dir.name) / config.usercode_entry_point
    with open(entry_point, 'wb') as out_file:
        content = in_file.file.read()
        out_file.write(content)

def _fix_bad_spools(spooled_file: fastapi.UploadFile):
    """Due to a python bug not all of the interfaces are compatible.
    The `fastapi.UploadFile` type inherits from `SpooledTemporaryFile` a builtin
    which does not specify the abstract for `IOBase`. There is some work to fix
    this:
    https://bugs.python.org/issue26175
    A fix for this has been merged in into the 3.11 rc so hopefully this will be
    fixed soon:
    https://github.com/python/cpython/commit/78e70be3318bc2ca57dac188061ed35017a0867c

    For now we reach in to the object to try and patch it ourselves.
    This will not work for files larger than `UploadFile._max_size` as the
    attributes change:
    https://stackoverflow.com/a/47169185/5006710

    We make sure that the object has a large enough size in
    main.increase_max_file_size
    """
    def readable(self):
        return self._file.readable

    def writable(self):
        return self._file.writable

    def seekable(self):
        return self._file.seekable

    spooled_file.file.seekable = types.MethodType(seekable, spooled_file.file)
    spooled_file.file.readable = types.MethodType(readable, spooled_file.file)
    spooled_file.file.writable = types.MethodType(writable, spooled_file.file)


def _stage_zip(dir: tempfile.TemporaryDirectory, in_file: fastapi.UploadFile):
    _fix_bad_spools(in_file)

    try:
        with zipfile.ZipFile(in_file.file, "r") as zip:
            zip.extractall(dir.name)
    except shutil.ReadError as e:
        raise e

    entry_path = (Path(dir.name) / config.usercode_entry_point)
    if not entry_path.exists():
        raise TypeError(f"Unable to find {config.usercode_entry_point} in zip")


@contextlib.contextmanager
def _stage_usecode(file: fastapi.UploadFile):
    """Create the usecode directory with the file structure ready for the runner
    Raises FileType errors if unable to process usercode.
    """
    try:
        tempdir = tempfile.TemporaryDirectory()
        if _is_python(file):
            _stage_python(tempdir, file)
        elif _is_zip(file):
            _stage_zip(tempdir, file)
        else:
            raise FileType("Unknown File type, upload `.zip` or `.py`")

        yield tempdir
    finally:
        tempdir.cleanup()


def process_uploaded_file(file: fastapi.UploadFile):
    """Does the mime type and linter all return good?"""
    with _stage_usecode(file) as staging_dir:
        runner.state = States.STOPPED
        shutil.rmtree(config.usercode_path)
        shutil.move(staging_dir.name, config.usercode_path)
        runner.state = States.INIT
