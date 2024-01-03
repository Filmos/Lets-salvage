import os
from typing import Callable, Generator
from reading.zip_glob_proxy import ZipGlobProxy
from pathlib import Path

class Reader:
    def __init__(self, path: str):
        self.path = path
        self.bindings: list[tuple[str, Callable]] = []

    def bind(self, name: str, function: Callable) -> 'Reader':
        self.bindings.append((name, function))
        return self

    def read(self) -> str:
        for mod in self.read_mods():
            prefix_len = len(mod.as_posix()) + 1
            for pattern, listener in self.bindings:
                for file in mod.glob(pattern):
                    with open(file, "r") as f:
                        content = f.read()
                    listener(file.as_posix()[prefix_len:], content)

    def read_mods(self) -> Generator[Path, None, None]:
        for file in os.listdir(self.path + "/mods"):
            with ZipGlobProxy(self.path + "/mods/" + file) as path:
                yield path

    def clone(self) -> 'Reader':
        return Reader(self.path)