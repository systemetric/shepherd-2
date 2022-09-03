"""Process an uploaded file"""
import contextlib
import shutil
import tempfile
import types
import zipfile
from pathlib import Path

import fastapi

from app.config import config
from app.run import States, runner


def _is_python(file: fastapi.UploadFile) -> bool:
    """Returns if `file` is likely a python file"""
    return file.content_type.startswith("text") or file.filename.endswith(".py")


def _is_zip(file: fastapi.UploadFile) -> bool:
    """Returns if `file` is likely a zip"""
    return (("zip" in file.content_type) or file.filename.endswith(".zip"))


def _stage_python(dir: tempfile.TemporaryDirectory, in_file: fastapi.UploadFile):
    """Place a python `in_file` in `dir`"""
    entry_point = Path(dir.name) / config.round_entry_point
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


def increase_max_file_size():
    """This is the maximum filesize which can be uploaded to shepherd.
    see app.upload._fix_bad_zips for more info.

    starlette which FastAPI uses does not allow for us to set the spool_max_size
    in the constructor instead defining it as a class attribute so we override
    this class attribute.

    We need to do this because of the bug in python see in _fix_bad_spools
    """
    from starlette.datastructures import UploadFile as StarletteUploadFile

    # the original size * a big number which we will never hit
    StarletteUploadFile.spool_max_size = (1024 * 1024) * 99999999999999999


def _stage_zip(dir: tempfile.TemporaryDirectory, in_file: fastapi.UploadFile):
    """Try and extract a zip `in_file` to `dir` and check it is a valid zip"""
    _fix_bad_spools(in_file)

    try:
        with zipfile.ZipFile(in_file.file, "r") as zip:
            zip.extractall(dir.name)
    except shutil.ReadError as e:
        raise e

    entry_path = (Path(dir.name) / config.round_entry_point)
    if not entry_path.exists():
        raise TypeError(f"Unable to find {config.round_entry_point} in zip")


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
        shutil.rmtree(config.round_path)
        shutil.move(staging_dir.name, config.round_path)
        runner.state = States.INIT
