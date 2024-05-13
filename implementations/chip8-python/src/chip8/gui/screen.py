from chip8.engine import Engine
import pygame

HI_COLOR = "yellow"
LO_COLOR = "orange"


class Screen:
    def process(self, engine: Engine, surface: pygame.Surface) -> None:
        surface.fill(LO_COLOR)

        for idx, value in enumerate(engine._display._data):
            x = idx % engine._display.SCREEN_SIZE_X
            y = idx // engine._display.SCREEN_SIZE_X
            surface.set_at((x, y), HI_COLOR if value == 1 else LO_COLOR)
