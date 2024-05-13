class Quirks:
    shift_y: bool
    add_i_carry: bool
    vf_reset: bool
    index_increment: bool
    draw_clipping: bool

    def __init__(self) -> None:
        self.shift_y = True
        self.add_i_carry = False
        self.vf_reset = True
        self.index_increment = True
        self.draw_clipping = True