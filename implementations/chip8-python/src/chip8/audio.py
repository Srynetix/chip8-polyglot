from chip8.types import Byte


class Audio:
    PATTERN_BUFFER_SIZE = 16

    _pattern_buffer: list[Byte]
    _pitch: Byte

    def __init__(self) -> None:
        self._pattern_buffer = [Byte(0) for _ in range(self.PATTERN_BUFFER_SIZE)]
        self._pitch = Byte(64)

    def set_pattern_buffer(self, buffer: list[Byte]) -> None:
        assert len(buffer) == 16
        self._pattern_buffer = buffer

    def set_pitch(self, value: Byte) -> None:
        self._pitch = value

    def reset(self) -> None:
        self._pattern_buffer.clear()

    @property
    def buffer(self) -> list[Byte]:
        return self._pattern_buffer

    @property
    def frequency(self) -> float:
        return 4000 * (2 ** ((self._pitch.value - 64) / 48))
