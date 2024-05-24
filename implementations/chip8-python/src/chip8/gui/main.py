import logging
from typing import Annotated, Optional
from chip8.gui.keyboard import Keyboard
from chip8.gui.screen import Screen
import pygame
from pathlib import Path
import typer

from chip8.gui.sound import Buzzer

from chip8.engine import Engine, StepResult
from chip8.mode import EmulationMode
from chip8.cartridge import Cartridge
from chip8.quirks import QuirksMode


def start_gui(engine: Engine) -> None:
    pygame.init()

    pygame.mixer.init()
    pygame.mixer.set_num_channels(1)

    pygame.display.set_caption(f"CHIP-8 (emulation mode: {engine._emulation_mode})")
    screen = pygame.display.set_mode((640, 320))
    clock = pygame.time.Clock()

    running = True
    paused = False

    gui_screen = Screen()
    gui_keyboard = Keyboard()

    beep_voice = pygame.mixer.Channel(0)
    buzzer = Buzzer()
    buzzer.generate(
        4000.0,
        [
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
        ],
    )

    pixel_surface = pygame.Surface((128, 64))

    @engine.on_loop.connect
    def on_loop():
        nonlocal paused

        print("End")
        paused = True

    @engine.on_exit.connect
    def on_exit():
        nonlocal paused

        print("Exit")
        paused = True

    @engine.on_audio_update.connect
    def on_audio_update(frequency: float, buffer: list[int]):
        print("update", frequency, buffer)
        buzzer.generate(frequency, buffer)
        beep_voice.stop()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.scancode == pygame.KSCAN_ESCAPE:
                    running = False

            gui_keyboard.process(engine, event)

        if not paused:
            result = engine.step()
            if result == StepResult.BadOpCode:
                raise RuntimeError("Bad opcode")

        if engine.beeping:
            if not beep_voice.get_busy():
                buzzer.play_on_voice(beep_voice)
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
    instructions_per_step: Optional[int] = None,
    # Quirks
    quirks_shift_y: Optional[bool] = None,
    quirks_add_i_carry: Optional[bool] = None,
    quirks_vf_reset: Optional[bool] = None,
    quirks_jump_vx: Optional[bool] = None,
    quirks_index_increment: Optional[bool] = None,
    quirks_draw_clipping: Optional[bool] = None,
    quirks_legacy_scrolling: Optional[bool] = None,
    quirks_display_wait: Optional[bool] = None,
    # Quirks mode
    quirks_mode: Annotated[
        QuirksMode | None, typer.Option(parser=QuirksMode.parse)
    ] = None,
    # Emulation mode
    emulation_mode: Annotated[
        EmulationMode | None, typer.Option(parser=EmulationMode.parse)
    ] = None,
):
    if verbose:
        logging.basicConfig(level=logging.INFO)

    engine = Engine()

    cartridge = Cartridge.from_path(cartridge_path)
    if emulation_mode is None:
        emulation_mode = EmulationMode.Chip8

    # Apply mode
    engine.set_emulation_mode(emulation_mode)

    # Apply quirks
    if emulation_mode == EmulationMode.Chip8:
        engine.quirks.apply_mode(QuirksMode.Chip8)
    elif emulation_mode == EmulationMode.SuperChip:
        engine.quirks.apply_mode(QuirksMode.SuperChipModern)
    elif emulation_mode == EmulationMode.XoChip:
        engine.quirks.apply_mode(QuirksMode.XoChip)

    if quirks_shift_y is not None:
        engine.quirks.shift_y = quirks_shift_y
    if quirks_add_i_carry is not None:
        engine.quirks.add_i_carry = quirks_add_i_carry
    if quirks_vf_reset is not None:
        engine.quirks.vf_reset = quirks_vf_reset
    if quirks_jump_vx is not None:
        engine.quirks.jump_vx = quirks_jump_vx
    if quirks_index_increment is not None:
        engine.quirks.index_increment = quirks_index_increment
    if quirks_draw_clipping is not None:
        engine.quirks.draw_clipping = quirks_draw_clipping
    if quirks_legacy_scrolling is not None:
        engine.quirks.legacy_scrolling = quirks_legacy_scrolling
    if quirks_display_wait is not None:
        engine.quirks.display_wait = quirks_display_wait

    if quirks_mode is not None:
        engine.quirks.apply_mode(quirks_mode)

    if instructions_per_step is not None:
        engine.set_instructions_per_step(instructions_per_step)

    engine.load_cartridge(cartridge)

    start_gui(engine)


if __name__ == "__main__":
    typer.run(main)
