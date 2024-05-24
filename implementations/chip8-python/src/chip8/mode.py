import enum


class EmulationMode(enum.StrEnum):
    Chip8 = "chip-8"
    SuperChip = "schip"
    XoChip = "xochip"

    @classmethod
    def parse(cls, value: str) -> "EmulationMode":
        return EmulationMode(value)
