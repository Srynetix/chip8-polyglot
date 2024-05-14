import enum


class QuirksMode(enum.StrEnum):
    Chip8 = "chip-8"
    SuperChipModern = "schip" 
    SuperChipLegacy = "schip-legacy"
    XoChip = "xochip"

    @classmethod
    def parse(cls, value: str) -> "QuirksMode":
        return QuirksMode(value)


class Quirks:
    shift_y: bool
    add_i_carry: bool
    vf_reset: bool
    index_increment: bool
    draw_clipping: bool
    jump_vx: bool
    legacy_scrolling: bool

    def __init__(self) -> None:
        self.shift_y = True
        self.add_i_carry = False
        self.vf_reset = True
        self.index_increment = True
        self.draw_clipping = True
        self.jump_vx = False
        self.legacy_scrolling = False

    def apply_mode(self, mode: QuirksMode) -> None:
        if mode == QuirksMode.Chip8:
            self.shift_y = True
            self.add_i_carry = False
            self.vf_reset = True
            self.index_increment = True
            self.draw_clipping = True
            self.jump_vx = False
            self.legacy_scrolling = False

        elif mode == QuirksMode.SuperChipModern:
            self.shift_y = False
            self.add_i_carry = True
            self.vf_reset = False
            self.index_increment = False
            self.draw_clipping = True
            self.jump_vx = True
            self.legacy_scrolling = False

        elif mode == QuirksMode.SuperChipLegacy:
            self.shift_y = False
            self.add_i_carry = True
            self.vf_reset = False
            self.index_increment = False
            self.draw_clipping = True
            self.jump_vx = True
            self.legacy_scrolling = True

        elif mode == QuirksMode.XoChip:
            raise NotImplementedError()