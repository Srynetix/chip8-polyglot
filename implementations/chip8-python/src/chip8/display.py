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
        v = value
        s0 = (v & 0b1000_0000) >> 7
        s1 = (v & 0b0100_0000) >> 6
        s2 = (v & 0b0010_0000) >> 5
        s3 = (v & 0b0001_0000) >> 4
        s4 = (v & 0b0000_1000) >> 3
        s5 = (v & 0b0000_0100) >> 2
        s6 = (v & 0b0000_0010) >> 1
        s7 = (v & 0b0000_0001)

        global_collision = False

        if self._draw_pixel(x, y, s0, clip=clip):
            global_collision = True

        if self._draw_pixel(x + 1, y, s1, clip=clip):
            global_collision = True

        if self._draw_pixel(x + 2, y, s2, clip=clip):
            global_collision = True
        
        if self._draw_pixel(x + 3, y, s3, clip=clip):
            global_collision = True

        if self._draw_pixel(x + 4, y, s4, clip=clip):
            global_collision = True

        if self._draw_pixel(x + 5, y, s5, clip=clip):
            global_collision = True

        if self._draw_pixel(x + 6, y, s6, clip=clip):
            global_collision = True

        if self._draw_pixel(x + 7, y, s7, clip=clip):
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