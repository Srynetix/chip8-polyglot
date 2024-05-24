import audioop
import struct
from typing import Generator

import pygame


class Buzzer:
    _sound: pygame.mixer.Sound | None
    _playback_time: int

    def __init__(self) -> None:
        self._sound = None
        self._playback_time = 0

    def _buffer_gen(self, pattern_buffer: list[int]) -> Generator[int, None, None]:
        for byte in pattern_buffer:
            for bit in range(8):
                bit_n = 1 << bit
                if byte & bit_n == bit_n:
                    yield 32767
                else:
                    yield -32767

    def generate(self, frequency: float, pattern_buffer: list[int]) -> None:
        generated_buffer = list(self._buffer_gen(pattern_buffer))
        packed_buffer = struct.pack(f"{len(generated_buffer)}h", *generated_buffer)

        new_samples, _ = audioop.ratecv(
            packed_buffer, 1, 1, int(frequency), pygame.mixer.get_init()[0], None
        )

        sound = pygame.mixer.Sound(buffer=new_samples)
        sound.set_volume(0.1)
        self._sound = sound

    def play_on_voice(self, voice: pygame.mixer.Channel) -> None:
        if self._sound:
            voice.play(self._sound)
