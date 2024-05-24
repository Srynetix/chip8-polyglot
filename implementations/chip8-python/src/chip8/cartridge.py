from pathlib import Path

from .types import Byte


class Cartridge:
    _data: list[Byte]

    def __init__(self, data: bytes) -> None:
        self._data = [Byte(d) for d in data]

    @classmethod
    def from_path(cls, path: Path):
        with open(path, mode="rb") as fd:
            return cls(fd.read())
