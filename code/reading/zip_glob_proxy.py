from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory


class ZipGlobProxy:
    def __init__(self, path: str):
        self.zipfile = ZipFile(path, "r")
        self.temp_directory = None
     
    def __enter__(self) -> Path:
        self.temp_directory = TemporaryDirectory()
        with self.zipfile as zipfile:
            zipfile.extractall(self.temp_directory.name)
        return Path(self.temp_directory.name)
 
    def __exit__(self, *args):
        self.temp_directory.cleanup()