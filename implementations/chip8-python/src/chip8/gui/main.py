import pygame
from pathlib import Path
import typer

from chip8.engine import Engine, StepResult
from chip8.types import Byte
from chip8.cartridge import Cartridge

HI_COLOR = "yellow"
LO_COLOR = "orange"
CYCLES_PER_FRAME = 8

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
    


def start_gui(engine: Engine) -> None:
    stepping = True

    pygame.init()
    pygame.display.set_caption("CHIP-8")
    screen = pygame.display.set_mode((640, 320))
    clock = pygame.time.Clock()
    running = True

    pixel_surface = pygame.Surface((64, 32))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.scancode in KEY_MAP.keys():
                    engine._keypad.set_kx(Byte(KEY_MAP[event.scancode]), True)

            elif event.type == pygame.KEYUP:
                if event.scancode in KEY_MAP.keys():
                    engine._keypad.set_kx(Byte(KEY_MAP[event.scancode]), False)


        pixel_surface.fill(LO_COLOR)

        for _ in range(CYCLES_PER_FRAME):
            if stepping:
                result = engine.step()
                if result == StepResult.BadOpCode:
                    raise RuntimeError("Bad opcode")
                elif result == StepResult.Loop:
                    print("Loop found")
                    stepping = False
                    break

        engine.step_timers()

        for idx, value in enumerate(engine._display._data):
            x = idx % engine._display.SCREEN_SIZE[0]
            y = idx // engine._display.SCREEN_SIZE[0]
            pixel_surface.set_at((x, y), HI_COLOR if value == 1 else LO_COLOR)

        pygame.transform.scale(pixel_surface, (640, 320), screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


def main(
        cartridge_path: Path,
        *,
        quirks_shift_y: bool = True,
        quirks_add_i_carry: bool = False,
        quirks_vf_reset: bool = True,
        quirks_index_increment: bool = True,
        quirks_draw_clipping: bool = True
    ):
    engine = Engine()
    engine._quirks._shift_y = quirks_shift_y
    engine._quirks._add_i_carry = quirks_add_i_carry
    engine._quirks._vf_reset = quirks_vf_reset
    engine._quirks._index_increment = quirks_index_increment
    engine._quirks._draw_clipping = quirks_draw_clipping

    cartridge = Cartridge.from_path(cartridge_path)
    engine.load_cartridge(cartridge)

    start_gui(engine)


if __name__ == "__main__":
    typer.run(main)