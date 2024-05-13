from dataclasses import dataclass


@dataclass
class Address:
    value: int

    def __init__(self, value: int) -> None:
        self.value = value % 65536

    def __repr__(self) -> str:
        return f"&{hex(self.value).upper()}"

    def __add__(self, other) -> "Address":
        return Address(self.value + other)


@dataclass
class Register:
    value: int

    def __init__(self, value: int) -> None:
        if value < 0 or value > 15:
            raise RuntimeError("Unsupported register value")
        self.value = value

    def __repr__(self) -> str:
        return f"V{hex(self.value)[2:].upper()}"


@dataclass
class Byte:
    value: int

    def __init__(self, value: int) -> None:
        self.value = value % 256

    def __repr__(self) -> str:
        return hex(self.value).upper()

    def __add__(self, other) -> "Byte":
        if isinstance(other, Byte):
            return Byte((self.value + other.value) % 256)
        if isinstance(other, int):
            return Byte((self.value + other) % 256)
        raise RuntimeError("Cannot add")

    def __or__(self, other) -> "Byte":
        if isinstance(other, Byte):
            return Byte(self.value | other.value)

    def __and__(self, other) -> "Byte":
        if isinstance(other, Byte):
            return Byte(self.value & other.value)

    def __xor__(self, other) -> "Byte":
        if isinstance(other, Byte):
            return Byte(self.value ^ other.value)