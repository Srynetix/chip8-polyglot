from .types import Byte, Address


class Memory:
    MEMORY_SIZE = 4096

    _data: list[Byte]

    def __init__(self) -> None:
        self._data = [Byte(0) for _ in range(self.MEMORY_SIZE)]

    def reset(self) -> None:
        for x in range(len(self._data)):
            self._data[x] = Byte(0)

    def store_memory(self, start: Address, memory: list[Byte]) -> None:
        if start.value + len(memory) > len(self._data):
            raise RuntimeError("Memory buffer overflow")

        for i in range(len(memory)):
            self._data[start.value + i] = memory[i]

    def read_memory(self, start: Address, count: Byte) -> list[Byte]:
        return self._data[start.value:start.value + count.value]

    def read_opcode(self, start: Address) -> Address:
        code_array = self._data[start.value:start.value + 2]
        return Address((code_array[0].value << 8) + code_array[1].value)
