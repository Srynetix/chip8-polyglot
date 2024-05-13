from .types import Address


class Stack:
    STACK_SIZE = 16

    _data: list[Address]

    def __init__(self) -> None:
        self._data = []

    def reset(self) -> None:
        self._data = []

    def pop_stack(self) -> Address:
        if len(self._data) == 0:
            raise RuntimeError("Empty stack")
        return self._data.pop()

    def push_stack(self, addr: Address) -> None:
        if len(self._data) == self.STACK_SIZE:
            raise RuntimeError("Stack full")
        self._data.append(addr)
