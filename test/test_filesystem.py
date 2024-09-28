from pathlib import Path
from uuid import uuid4
from shutil import copyfile

import pytest

from src.file_system import FileSystem

ASSETS_TAR = Path("test/assets/aboba.tar")


@pytest.fixture
def temp_fs() -> FileSystem:
    new_name = Path(uuid4().hex + ".tar")
    copyfile(ASSETS_TAR, new_name)
    fs = FileSystem(new_name)
    yield fs

    fs.close()
    new_name.unlink()


def test_pwd(temp_fs: FileSystem) -> None:
    assert temp_fs.pwd() == "/"


def test_cd(temp_fs: FileSystem) -> None:
    temp_fs.cd(["cd"])
    assert temp_fs.pwd() == "/"


def test_cd_slash(temp_fs: FileSystem) -> None:
    temp_fs.cd(["cd", "/"])
    assert temp_fs.pwd() == "/"


def test_cd_catalog(temp_fs: FileSystem) -> None:
    temp_fs.cd(["cd", "dir1"])
    assert temp_fs.pwd() == "/dir1/"


def test_rmdir(temp_fs: FileSystem) -> None:
    temp_fs.rmdir("dir1")

    for member in temp_fs._files.getmembers():
        if member.name.startswith(temp_fs._vpath_to_real("dir1")[:-1]):
            assert not False


def test_rmdir_with_slash(temp_fs: FileSystem) -> None:
    temp_fs.rmdir("dir1/")

    for member in temp_fs._files.getmembers():
        if member.name.startswith(temp_fs._vpath_to_real("dir1")[:-1]):
            assert not False


def test_ls(temp_fs: FileSystem) -> None:
    res = temp_fs.ls(["ls", "dir1/"])
    assert repr(res) == r"'File name\t\t\t\tSize\ndestroy_sql.sql\t\t\t\t0\n'"


def test_ls_home(temp_fs: FileSystem) -> None:
    res = temp_fs.ls(["ls", "."])
    assert repr(res) == r"'File name\t\t\t\tSize\ndir1/\t\t\t\t0\ndir2/\t\t\t\t0\nhack_pentagon.py\t\t\t\t57\nCON\t\t\t\t0\n'"
