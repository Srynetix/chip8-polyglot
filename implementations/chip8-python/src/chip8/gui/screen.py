from chip8.engine import Engine
import pygame

HI_COLOR = "yellow"
LO_COLOR = "darkgoldenrod4"
HI2_COLOR = "orange"
OVERLAP_COLOR = "darkorange4"


class Screen:
    def process(self, engine: Engine, surface: pygame.Surface) -> None:
        surface.fill(LO_COLOR)

        screen_x = engine._display.SCREEN_SIZE_X
        for idx, value in enumerate(engine._display.planes[0]):
            x = idx % screen_x
            y = idx // screen_x
            surface.set_at((x, y), HI_COLOR if value == 1 else LO_COLOR)

        for idx, value in enumerate(engine._display.planes[1]):
            value0 = engine._display.planes[0][idx]
            x = idx % screen_x
            y = idx // screen_x

            if value == 1 and value0 == 1:
                surface.set_at((x, y), OVERLAP_COLOR)
            elif value == 1 and value0 == 0:
                surface.set_at((x, y), HI2_COLOR)
