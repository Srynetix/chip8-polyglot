# Timers should run 60 times per second
from .types import Byte


class Timers:
    _delay_timer: Byte
    _sound_timer: Byte

    def __init__(self) -> None:
        self._delay_timer = Byte(0)
        self._sound_timer = Byte(0)

    def reset(self) -> None:
        self._delay_timer = Byte(0)
        self._sound_timer = Byte(0)

    def step(self) -> None:
        if self._delay_timer > 0:
            self._delay_timer -= 1
     
        if self._sound_timer > 0:
            self._sound_timer -= 1

    def set_delay_timer(self, value: Byte) -> None:
        self._delay_timer = value

    def set_sound_timer(self, value: Byte) -> None:
        self._sound_timer = value
    
    @property
    def sound_timer(self) -> Byte:
        return self._sound_timer

    @property
    def delay_timer(self) -> Byte:
        return self._delay_timer