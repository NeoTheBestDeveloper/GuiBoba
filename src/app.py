from tkinter import Tk, Text
import tkinter as tk
from pathlib import Path

from src.file_system import FileSystem
from src.position import Position

__all__ = [
    "App",
]


class App:
    _window: Tk
    _command_input: Text
    _fs: FileSystem
    _ps1: str = "[{hostname} {pwd} ]$ "
    _hostname: str

    _current_cmd_pos: Position
    _prev_cmd_pos: Position

    def __init__(self, path: Path, hostname: str, title: str = "NeoTerm") -> None:
        self._hostname = hostname
        self._window = Tk()
        self._fs = FileSystem(path)

        self._setup(title)
        self._bindings()

        self._current_cmd_pos = Position(f"1.{len(self.ps1)}")
        self._prev_cmd_pos = self._current_cmd_pos

    def _setup(self, title: str) -> None:
        self._window.attributes("-alpha", 0.6)
        self._window.title(title)
        self._window.resizable(False, False)
        self._window.config(cursor="none")
        self._command_input = Text(master=self._window)
        self._command_input.insert(tk.END, self.ps1)

    def _bindings(self) -> None:
        def handle_keypress(event) -> None:
            if event.keysym == "Return":
                self._execute()

        self._window.bind("<Key>", handle_keypress)

        def check_pos(event):
            self._current_cmd_pos = Position(self._command_input.index(tk.INSERT))

        self._command_input.bindtags(('Text', 'post-class-bindings', '.', 'all'))

        self._command_input.bind_class("post-class-bindings", "<KeyPress>", check_pos)
        self._command_input.bind_class("post-class-bindings", "<Button-1>", check_pos)

    def _pack(self) -> None:
        self._command_input.pack()

    def _execute(self) -> None:
        cmd = self._command_input.get(str(self._prev_cmd_pos), tk.END)[:-2]
        args = cmd.split()

        match args[0]:
            case "ls":
                output = self._fs.ls(args)
                self._print(output + "\n")
            case "pwd":
                output = self._fs.pwd()
                self._print(output + "\n")
            case "cd":
                output = self._fs.cd(args)
                if output:
                    self._print(output + "\n")
            case "clear":
                self._clear()
            case "rmdir":
                self._fs.rmdir(args[1])
            case "exit":
                self._exit()
            case _:
                self._print("Неверная команда\n")

        self._print(self.ps1)
        self._prev_cmd_pos = self._current_cmd_pos

    def _clear(self) -> None:
        self._command_input.delete("1.0", tk.END)
        self._current_cmd_pos = Position(f"1.0")
        self._prev_cmd_pos = self._current_cmd_pos

    def _exit(self) -> None:
        self._window.destroy()

    def _print(self, string: str) -> None:
        self._command_input.insert(tk.END, string)

        if "\n" in string:
            self._current_cmd_pos.add_rows(string.count("\n"))
        else:
            self._current_cmd_pos.add_cols(len(string))

    @property
    def ps1(self) -> str:
        return self._ps1.format(pwd=self._fs.pwd(), hostname=self._hostname)

    def run(self) -> None:
        self._pack()
        self._window.mainloop()
