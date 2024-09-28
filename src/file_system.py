import os
import tarfile
from pathlib import Path

__all__ = [
    "FileSystem",
]


class FileSystem:
    _files: tarfile.TarFile
    _pwd: str
    _pwd_prefix: str
    _path: Path

    def __init__(self, path: Path) -> None:
        self._path = path
        self._files = tarfile.open(path, "r:*")
        self._pwd_prefix = self._files.getmembers()[0].name
        self._pwd = "/"

    def _vpath_to_real(self, path: str) -> str:
        path = path if path.endswith("/") else path + "/"

        if path == ".":
            return f"{self._pwd_prefix}{self._pwd}"
        elif path.startswith("./"):
            return f"{self._pwd_prefix}{self._pwd}{path[2:]}"
        elif path.startswith("/"):
            return f"{self._pwd_prefix}{path}"
        return f"{self._pwd_prefix}{self._pwd}{path}"

    def ls(self, args: list[str]) -> str:
        if len(args) == 1:
            argument = "."
        else:
            argument = args[1]
        path = self._vpath_to_real(argument)

        try:
            self._files.getmember(path)
        except KeyError:
            return f"File or directory does not exist: {args[1]}"

        output = "File name\t\t\t\tSize\n"
        for tarinfo in self._files:
            name_without_prefix = tarinfo.name.replace(path, "")
            if tarinfo.name.startswith(path) and "/" not in name_without_prefix:
                file_name = tarinfo.name.split("/")[-1]
                if tarinfo.isdir():
                    file_name += "/"
                output += f"{file_name}\t\t\t\t{tarinfo.size}\n"

        return output

    def cd(self, args: list[str]) -> str:
        if len(args) == 1:
            return ""

        new_path = args[1]

        if not new_path.endswith("/"):
            new_path += "/"
        if not new_path.startswith("/"):
            new_path = "/" + new_path
        self._pwd = new_path

        return ""

    def rmdir(self, path_to_delete: str) -> None:
        self._remove_directory_from_tar(path_to_delete)

    def _remove_directory_from_tar(self, dir_to_remove: str) -> None:
        temp_tar_path = Path(str(self._path) + ".tmp")

        new_tar = tarfile.open(temp_tar_path, 'w')
        for member in self._files.getmembers():
            if not member.name.startswith(self._vpath_to_real(dir_to_remove)[:-1]):
                new_tar.addfile(member, self._files.extractfile(member))

        self._files.close()
        self._path.unlink()

        new_tar.close()
        temp_tar_path.rename(str(self._path))
        temp_tar_path = self._path

        self._files = tarfile.open(temp_tar_path, "r:*")

    def pwd(self) -> str:
        return self._pwd

    def close(self) -> None:
        self._files.close()