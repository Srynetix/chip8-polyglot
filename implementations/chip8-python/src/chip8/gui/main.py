import logging
from chip8.gui.keyboard import Keyboard
from chip8.gui.screen import Screen
import pygame
from pathlib import Path
import typer

from chip8.engine import Engine, StepResult
from chip8.types import Byte
from chip8.cartridge import Cartridge

from chip8.gui.sound import Tone


CYCLES_PER_FRAME = 8  # 8 * 60 => 480 CPS


def start_gui(engine: Engine) -> None:
    stepping = True

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.set_num_channels(1)

    pygame.display.set_caption("CHIP-8")
    screen = pygame.display.set_mode((640, 320))
    clock = pygame.time.Clock()

    running = True

    gui_screen = Screen()    
    gui_keyboard = Keyboard()

    beep_voice = pygame.mixer.Channel(0)
    tone = Tone(frequency=220)

    pixel_surface = pygame.Surface((64, 32))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            gui_keyboard.process(engine, event)

        for _ in range(CYCLES_PER_FRAME):
            if stepping:
                result = engine.step()
                if result == StepResult.BadOpCode:
                    raise RuntimeError("Bad opcode")
                elif result == StepResult.Loop:
                    print("Loop found, stopping.")
                    stepping = False
                    break

        if engine.beeping:
            if not beep_voice.get_busy():
                beep_voice.play(tone, -1)
        else:
            beep_voice.stop()

        engine.step_timers()

        gui_screen.process(engine, pixel_surface)

        pygame.transform.scale(pixel_surface, (640, 320), screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.mixer.quit()
    pygame.quit()


def main(
        cartridge_path: Path,
        *,
        verbose: bool = False,
        quirks_shift_y: bool = True,
        quirks_add_i_carry: bool = False,
        quirks_vf_reset: bool = True,
        quirks_index_increment: bool = True,
        quirks_draw_clipping: bool = True
    ):

    if verbose:
        logging.basicConfig(level=logging.INFO)

    engine = Engine()
    engine.quirks.shift_y = quirks_shift_y
    engine.quirks.add_i_carry = quirks_add_i_carry
    engine.quirks.vf_reset = quirks_vf_reset
    engine.quirks.index_increment = quirks_index_increment
    engine.quirks.draw_clipping = quirks_draw_clipping

    cartridge = Cartridge.from_path(cartridge_path)
    engine.load_cartridge(cartridge)

    start_gui(engine)


if __name__ == "__main__":
    typer.run(main)