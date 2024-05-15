from pathlib import Path

from chip8.quirks import QuirksMode

from .types import Address, Byte


class Cartridge:
    _data: list[Byte]

    def __init__(self, data: bytes) -> None:
        self._data = [Byte(d) for d in data]

    @classmethod
    def from_path(cls, path: Path):
        with open(path, mode="rb") as fd:
            return cls(fd.read())

    def detect_quirks_mode(self) -> QuirksMode:
        for i in range(1, len(self._data)):
            addr = Address.from_bytes(self._data[i - 1], self._data[i])
            if addr in [0x00FE, 0x00FF, 0x00FB, 0x00FC]:
                # That's a S-CHIP code, so suppose that's a S-CHIP game
                return QuirksMode.SuperChipModern

        # Nothing found, suppose CHIP-8
        return QuirksMode.Chip8
