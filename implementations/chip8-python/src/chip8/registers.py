from .types import Register, Address, Byte


class Registers:
    GENERAL_REGISTER_COUNT = 16
    INITIAL_PC = Address(0x200)

    _general: list[Byte]
    _i: Address
    _pc: Address

    def __init__(self) -> None:
        self._general = [Byte(0) for _ in range(self.GENERAL_REGISTER_COUNT)]
        self._i = Address(0x0)
        self._pc = self.INITIAL_PC

    def reset(self) -> None:
        for x in range(len(self._general)):
            self._general[x] = Byte(0)

        self._i = Address(0x0)
        self._pc = self.INITIAL_PC

    def set_pc(self, value: Address) -> None:
        self._pc = value

    def set_i(self, value: Address) -> None:
        self._i = value

    def increment_pc(self) -> None:
        self._pc.value += 2

    @property
    def pc(self) -> Address:
        return self._pc

    @property
    def i(self) -> Address:
        return self._i

    def get_vx(self, index: Register) -> Byte:
        if index.value > self.GENERAL_REGISTER_COUNT:
            raise RuntimeError("Unsupported general register.")
        return self._general[index.value]

    def set_vx(self, index: Register, value: Byte) -> None:
        if index.value > self.GENERAL_REGISTER_COUNT:
            raise RuntimeError("Unsupported general register.")
        self._general[index.value] = value

    def set_carry(self, value: bool) -> None:
        self._general[0xF] = Byte(int(value))