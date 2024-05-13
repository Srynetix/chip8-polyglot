class Quirks:
    _shift_y: bool
    _add_i_carry: bool
    _vf_reset: bool
    _index_increment: bool
    _draw_clipping: bool

    def __init__(self) -> None:
        self._shift_y = True
        self._add_i_carry = False
        self._vf_reset = True
        self._index_increment = True
        self._draw_clipping = True
