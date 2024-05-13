import logging
from .types import Register, Address, Byte

logger = logging.getLogger(__name__)


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
        prev_pc = self._pc
        self._pc = value
        logger.info(f" [set_pc({value})] {prev_pc} -> {value}")

    def set_i(self, value: Address) -> None:
        prev_i = self._i
        self._i = value
        logger.info(f" [set_i({value})] {prev_i} -> {value}")

    def increment_pc(self) -> None:
        prev_pc = self._pc
        self._pc += 2
        logger.info(f" [increment_pc] {prev_pc} -> {self._pc}")

    @property
    def pc(self) -> Address:
        return self._pc

    @property
    def i(self) -> Address:
        return self._i

    def get_vx(self, index: Register) -> Byte:
        if index > self.GENERAL_REGISTER_COUNT:
            raise RuntimeError("Unsupported general register.")
        return self._general[index.value]

    def set_vx(self, index: Register, value: Byte) -> None:
        if index > self.GENERAL_REGISTER_COUNT:
            raise RuntimeError("Unsupported general register.")
        
        prev_vx = self._general[index.value]
        self._general[index.value] = value
        logger.info(f" [set_vx({index}, {value})] {prev_vx} -> {value}")

    def set_carry(self, value: bool) -> None:
        prev_vx = self._general[0xF]
        self._general[0xF] = Byte(int(value))
        logger.info(f" [set_carry({value})] {prev_vx} -> {Byte(int(value))}")