from .types import Byte

class Keypad:
    KEYS_COUNT = 16
    RELEASE_TICKS = 2

    _state: list[bool]
    _last_released_key: Byte | None
    _last_released_key_ticks: int
    _ticks: int

    def __init__(self) -> None:
        self._state = [False for _ in range(self.KEYS_COUNT)]
        self._last_released_key = None
        self._last_released_key_ticks = 0
        self._ticks = 0

    def reset(self) -> None:
        for x in range(self.KEYS_COUNT):
            self._state[x] = False
        self._ticks = 0
        self._last_released_key = None
        self._last_released_key_ticks = 0

    def set_kx(self, key: Byte, value: bool) -> None:
        if key < 0 or key > 15:
            raise RuntimeError("Unsupported key value")

        self._state[key.value] = value

        if not value:
            self._last_released_key = key
            self._last_released_key_ticks = self._ticks

    def get_kx(self, key: Byte) -> bool:
        if key < 0 or key > 15:
            raise RuntimeError("Unsupported key value")
        return self._state[key.value]

    def step(self) -> None:
        if self._last_released_key and self._ticks - self._last_released_key_ticks > self.RELEASE_TICKS:
            self._last_released_key = None
        self._ticks += 1