from .types import Byte

class Display:
    SCREEN_SIZE = (64, 32)

    _data: list[int]

    def __init__(self) -> None:
        self._data = [0 for _ in range(self.SCREEN_SIZE[0] * self.SCREEN_SIZE[1])]

    def reset(self) -> None:
        for x in range(len(self._data)):
            self._data[x] = 0

    def draw(self, x: int, y: int, sprite_lines: list[Byte], *, clip: bool = True) -> bool:
        if x >= self.SCREEN_SIZE[0] or y >= self.SCREEN_SIZE[1]:
            # Disable clipping if out of bounds
            clip = False

        collision = False
        for line_idx, line in enumerate(sprite_lines):
            if self._draw_line(x, y + line_idx, line.value, clip=clip):
                collision = True

        return collision

    def _draw_line(self, x: int, y: int, value: int, *, clip: bool) -> bool:
        line_size = 8

        global_collision = False
        for i in range(line_size):
            pixel_value = (value & (0b1 << (line_size - i - 1))) >> (line_size - i - 1)
            if self._draw_pixel(x + i, y, pixel_value, clip=clip):
                global_collision = True

        return global_collision

    def _draw_pixel(self, x: int, y: int, value: int, *, clip: bool) -> bool:
        if clip and (x >= self.SCREEN_SIZE[0] or y >= self.SCREEN_SIZE[1]):
            return False

        index = self._xy_to_index(x % self.SCREEN_SIZE[0], y % self.SCREEN_SIZE[1])
        collision = False
        existing = self._data[index]
        if existing == 1 and value == 1:
            collision = True

        self._data[index] ^= value
        return collision

    def _xy_to_index(self, x: int, y: int) -> int:
        return x + y * self.SCREEN_SIZE[0]