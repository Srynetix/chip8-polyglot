import enum
import logging
from .types import Byte

logger = logging.getLogger(__name__)


class Display:
    class Mode(enum.Enum):
        LORES = "lores"
        HIRES = "hires"

    SCREEN_SIZE = (SCREEN_SIZE_X, SCREEN_SIZE_Y) = (128, 64)
    PLANES_COUNT = 2

    _planes: list[list[int]]
    _plane_mask: int
    _mode: Mode

    def __init__(self) -> None:
        self._planes = [
            [0 for _ in range(self.SCREEN_SIZE_X * self.SCREEN_SIZE_Y)]
            for _ in range(self.PLANES_COUNT)
        ]
        self._plane_mask = 0b01
        self._mode = self.Mode.LORES

    @property
    def planes(self) -> list[list[int]]:
        return self._planes

    def set_mode(self, mode: Mode) -> None:
        self._mode = mode

    def reset(self) -> None:
        for plane_idx in range(self.PLANES_COUNT):
            self._clear_plane(plane_idx)

        self._plane_mask = 0b1
        self._mode = self.Mode.LORES

    def clear(self) -> None:
        for plane_idx in self._plane_mask_to_indices():
            self._clear_plane(plane_idx)

    def set_plane_mask(self, mask: Byte) -> None:
        assert mask.value >= 0 and mask.value <= 3

        self._plane_mask = mask.value

    def draw(self, x: int, y: int, sprite: list[Byte], *, clip: bool = True) -> bool:
        collision = False
        for plane_idx in self._plane_mask_to_indices()[:1]:
            plane = self._planes[plane_idx]
            if self._draw_plane(plane, x, y, sprite, clip=clip):
                collision = True
        return collision

    def draw_multiplane(
        self, x: int, y: int, sprite_dual: list[Byte], *, clip: bool = True
    ) -> bool:
        collision = self._draw_plane(
            self._planes[0], x, y, sprite_dual[: len(sprite_dual) // 2], clip=clip
        )
        collision |= self._draw_plane(
            self._planes[1], x, y, sprite_dual[len(sprite_dual) // 2 :], clip=clip
        )
        return collision

    def super_draw(
        self, x: int, y: int, sprite: list[Byte], *, clip: bool = True
    ) -> bool:
        collision = False
        for plane_idx in self._plane_mask_to_indices()[:1]:
            plane = self._planes[plane_idx]
            if self._super_draw_plane(plane, x, y, sprite, clip=clip):
                collision = True
        return collision

    def super_draw_multiplane(
        self, x: int, y: int, sprite_dual: list[Byte], *, clip: bool = True
    ) -> bool:
        collision = self._super_draw_plane(
            self._planes[0], x, y, sprite_dual[: len(sprite_dual) // 2], clip=clip
        )
        collision |= self._super_draw_plane(
            self._planes[1], x, y, sprite_dual[len(sprite_dual) // 2 :], clip=clip
        )
        return collision

    def scroll_right(self, *, legacy_mode: bool) -> None:
        for plane_idx in self._plane_mask_to_indices():
            plane = self._planes[plane_idx]

            amount = 4
            if self._mode == self.Mode.LORES:
                if not legacy_mode:
                    amount *= 2

            for y in range(self.SCREEN_SIZE_Y - 1, -1, -1):
                for x in range(self.SCREEN_SIZE_X - 1, -1, -1):
                    src_index = self._xy_to_index(x, y)
                    dst_index = self._xy_to_index(x - amount, y)
                    plane[src_index] = plane[dst_index] if dst_index >= 0 else 0

    def scroll_left(self, *, legacy_mode: bool) -> None:
        for plane_idx in self._plane_mask_to_indices():
            plane = self._planes[plane_idx]

            amount = 4
            if self._mode == self.Mode.LORES:
                if not legacy_mode:
                    amount *= 2

            for y in range(self.SCREEN_SIZE_Y):
                for x in range(self.SCREEN_SIZE_X):
                    src_index = self._xy_to_index(x, y)
                    dst_index = self._xy_to_index(x + amount, y)
                    plane[src_index] = (
                        plane[dst_index]
                        if dst_index < self.SCREEN_SIZE_X * self.SCREEN_SIZE_Y
                        else 0
                    )

    def scroll_down(self, amount: Byte, *, legacy_mode: bool) -> None:
        assert amount >= 0 and amount < 16

        for plane_idx in self._plane_mask_to_indices():
            plane = self._planes[plane_idx]

            if self._mode == self.Mode.LORES:
                if not legacy_mode:
                    amount *= 2

            for y in range(self.SCREEN_SIZE_Y - 1, -1, -1):
                for x in range(self.SCREEN_SIZE_X - 1, -1, -1):
                    src_index = self._xy_to_index(x, y)
                    dst_index = self._xy_to_index(x, y - amount.value)
                    plane[src_index] = plane[dst_index] if dst_index >= 0 else 0

    def scroll_up(self, amount: Byte) -> None:
        assert amount >= 0 and amount < 16

        for plane_idx in self._plane_mask_to_indices():
            plane = self._planes[plane_idx]

            if self._mode == self.Mode.LORES:
                amount *= 2

            for y in range(self.SCREEN_SIZE_Y):
                for x in range(self.SCREEN_SIZE_X):
                    src_index = self._xy_to_index(x, y)
                    dst_index = self._xy_to_index(x, y + amount.value)
                    plane[src_index] = (
                        plane[dst_index]
                        if dst_index < self.SCREEN_SIZE_X * self.SCREEN_SIZE_Y
                        else 0
                    )

    def _draw_factor(self) -> int:
        return 2 if self._mode == self.Mode.LORES else 1

    def _plane_mask_to_indices(self) -> list[int]:
        if self._plane_mask == 0b1:
            return [0]
        elif self._plane_mask == 0b10:
            return [1]
        else:
            return [0, 1]

    def _clear_plane(self, plane_idx: int) -> None:
        for x in range(len(self._planes[plane_idx])):
            self._planes[plane_idx][x] = 0

    def _draw_plane(
        self, plane: list[int], x: int, y: int, sprite: list[Byte], *, clip: bool = True
    ) -> bool:
        factor = self._draw_factor()

        if x * factor >= self.SCREEN_SIZE_X or y * factor >= self.SCREEN_SIZE_Y:
            # Disable clipping if initially out of bounds
            clip = False

        collision = False
        for line_idx, line in enumerate(sprite):
            if self._draw_line(
                plane,
                x * factor,
                y * factor + line_idx * factor,
                line.value,
                factor=factor,
                clip=clip,
            ):
                collision = True

        return collision

    def _draw_line(
        self, plane: list[int], x: int, y: int, value: int, *, factor: int, clip: bool
    ) -> bool:
        line_size = 8

        global_collision = False
        for i in range(line_size):
            pixel_value = (value & (0b1 << (line_size - i - 1))) >> (line_size - i - 1)
            if self._draw_pixel(
                plane, x + i * factor, y, pixel_value, factor=factor, clip=clip
            ):
                global_collision = True

        return global_collision

    def _draw_pixel(
        self, plane: list[int], x: int, y: int, value: int, *, factor: int, clip: bool
    ) -> bool:
        if clip and (x >= self.SCREEN_SIZE_X or y >= self.SCREEN_SIZE_Y):
            return False

        collision = False

        for oy in range(factor):
            for ox in range(factor):
                index = self._xy_to_index(
                    (x + ox) % self.SCREEN_SIZE_X, (y + oy) % self.SCREEN_SIZE_Y
                )
                existing = plane[index]
                if existing == 1 and value == 1:
                    collision = True

                plane[index] ^= value

        return collision

    def _super_draw_plane(
        self, plane: list[int], x: int, y: int, sprite: list[Byte], *, clip: bool = True
    ) -> bool:
        factor = self._draw_factor()

        if x * factor >= self.SCREEN_SIZE_X or y * factor >= self.SCREEN_SIZE_Y:
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
            if self._draw_line(
                plane,
                x * factor,
                y * factor + line_idx * factor,
                half_1.value,
                factor=factor,
                clip=clip,
            ):
                collision = True

            if self._draw_line(
                plane,
                x * factor + 8 * factor,
                y * factor + line_idx * factor,
                half_2.value,
                factor=factor,
                clip=clip,
            ):
                collision = True

        return collision

    def _xy_to_index(self, x: int, y: int) -> int:
        return x + y * self.SCREEN_SIZE_X
