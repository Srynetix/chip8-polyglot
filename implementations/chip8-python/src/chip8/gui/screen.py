from chip8.engine import Engine
import pygame

HI_COLOR = "yellow"
LO_COLOR = "orange"


class Screen:
    def process(self, engine: Engine, surface: pygame.Surface) -> None:
        surface.fill(LO_COLOR)

        screen_x = engine._display.SCREEN_SIZE_X
        for idx, value in enumerate(engine._display.data):
            x = idx % screen_x
            y = idx // screen_x
            surface.set_at((x, y), HI_COLOR if value == 1 else LO_COLOR)
