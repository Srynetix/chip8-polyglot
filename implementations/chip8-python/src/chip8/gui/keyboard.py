from chip8.engine import Engine
from chip8.types import Byte
import pygame


KEY_MAP = {
    pygame.KSCAN_1: 0x1,
    pygame.KSCAN_2: 0x2,
    pygame.KSCAN_3: 0x3,
    pygame.KSCAN_4: 0xC,
    pygame.KSCAN_Q: 0x4,
    pygame.KSCAN_W: 0x5,
    pygame.KSCAN_E: 0x6,
    pygame.KSCAN_R: 0xD,
    pygame.KSCAN_A: 0x7,
    pygame.KSCAN_S: 0x8,
    pygame.KSCAN_D: 0x9,
    pygame.KSCAN_F: 0xE,
    pygame.KSCAN_Z: 0xA,
    pygame.KSCAN_X: 0x0,
    pygame.KSCAN_C: 0xB,
    pygame.KSCAN_V: 0xF,
}


class Keyboard:
    def process(self, engine: Engine, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.scancode in KEY_MAP.keys():
                engine._keypad.set_kx(Byte(KEY_MAP[event.scancode]), True)

        if event.type == pygame.KEYUP:
            if event.scancode in KEY_MAP.keys():
                engine._keypad.set_kx(Byte(KEY_MAP[event.scancode]), False)
