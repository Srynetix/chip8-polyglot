import enum
import logging
from .types import Byte

logger = logging.getLogger(__name__)


class Display:
    class Mode(enum.Enum):
        LORES = "lores"
        HIRES = "hires"

    SCREEN_SIZE = (
        SCREEN_SIZE_X,
        SCREEN_SIZE_Y
    ) = (128, 64)

    @property
    def screen_size(self) -> tuple[int, int]:
        return self.SCREEN_SIZE
        
    @property
    def pixels(self) -> list[int]:
        return self._data
        
    def set_mode(self, mode: Mode) -> None:
        self._mode = mode
        
    _data: list[int]
    _mode: Mode

    def _draw_factor(self) -> int:
        return 2 if self._mode == self.Mode.LORES else 1

    def __init__(self) -> None:
        self._data = [0 for _ in range(self.SCREEN_SIZE_X * self.SCREEN_SIZE_Y)]
        self._mode = self.Mode.LORES

    def reset(self) -> None:
        self.clear()
        self._mode = self.Mode.LORES

    def clear(self) -> None:
        for x in range(len(self._data)):
            self._data[x] = 0

    def draw(self, x: int, y: int, sprite: list[Byte], *, clip: bool = True) -> bool:
        factor = self._draw_factor()

        screen_x, screen_y = self.screen_size
        if x * factor >= screen_x or y * factor >= screen_y:
            # Disable clipping if initially out of bounds
            clip = False

        collision = False
        for line_idx, line in enumerate(sprite):
            if self._draw_line(x * factor, y * factor + line_idx * factor, line.value, factor=factor, clip=clip):
                collision = True

        return collision
    
    def super_draw(self, x: int, y: int, sprite: list[Byte], *, clip: bool = True) -> bool:
        if x >= self.SCREEN_SIZE_X or y >= self.SCREEN_SIZE_Y:
            clip = False

        sprite_lines = []
        current_line = []
        for line_idx, line in enumerate(sprite):
            current_line.append(line)
            if line_idx % 2 == 1:
                sprite_lines.append(current_line)
                current_line = []

        collision = False
        for line_idx, line in enumerate(sprite_lines):
            half_1, half_2 = line
            if self._draw_line(x, y + line_idx, half_1.value, factor=1, clip=clip):
                collision = True

            if self._draw_line(x + 8, y + line_idx, half_2.value, factor=1, clip=clip):
                collision = True

        return collision

    def scroll_right(self, *, legacy_mode: bool) -> None:
        amount = 4
        if self._mode == self.Mode.LORES:
            if not legacy_mode:
                amount *= 2

        for y in range(self.SCREEN_SIZE_Y - 1, -1, -1):
            for x in range(self.SCREEN_SIZE_X - 1, -1, -1):
                src_index = self._xy_to_index(x, y)
                dst_index = self._xy_to_index(x - amount, y)
                self._data[src_index] = self._data[dst_index] if dst_index >= 0 else 0

    def scroll_left(self, *, legacy_mode: bool) -> None:
        amount = 4
        if self._mode == self.Mode.LORES:
            if not legacy_mode:
                amount *= 2

        for y in range(self.SCREEN_SIZE_Y):
            for x in range(self.SCREEN_SIZE_X):
                src_index = self._xy_to_index(x, y)
                dst_index = self._xy_to_index(x + amount, y)
                self._data[src_index] = self._data[dst_index] if dst_index < self.SCREEN_SIZE_X * self.SCREEN_SIZE_Y else 0

    def scroll_down(self, amount: Byte, *, legacy_mode: bool) -> None:
        assert amount >= 0 and amount < 16

        if self._mode == self.Mode.LORES:
            if not legacy_mode:
                amount *= 2

        for y in range(self.SCREEN_SIZE_Y - 1, -1, -1):
            for x in range(self.SCREEN_SIZE_X - 1, -1, -1):
                src_index = self._xy_to_index(x, y)
                dst_index = self._xy_to_index(x, y - amount.value)
                self._data[src_index] = self._data[dst_index] if dst_index >= 0 else 0
    
    def _draw_line(self, x: int, y: int, value: int, *, factor: int, clip: bool) -> bool:
        line_size = 8

        global_collision = False
        for i in range(line_size):
            pixel_value = (value & (0b1 << (line_size - i - 1))) >> (line_size - i - 1)
            if self._draw_pixel(x + i * factor, y, pixel_value, factor=factor, clip=clip):
                global_collision = True

        return global_collision

    def _draw_pixel(self, x: int, y: int, value: int, *, factor: int, clip: bool) -> bool:
        screen_x, screen_y = self.screen_size

        if clip and (x >= screen_x or y >= screen_y):
            return False

        collision = False

        for oy in range(factor):
            for ox in range(factor):
                index = self._xy_to_index((x + ox) % screen_x, (y + oy) % screen_y)
                existing = self._data[index]
                if existing == 1 and value == 1:
                    collision = True

                self._data[index] ^= value

        return collision

    def _xy_to_index(self, x: int, y: int) -> int:
        return x + y * self.screen_size[0]