from typing import Any, Callable
import weakref


class Signal:
    _callbacks: list[weakref.ref]

    def __init__(self) -> None:
        self._callbacks = []

    def connect(self, callback: Callable[..., Any]) -> None:
        self._callbacks.append(weakref.ref(callback))
        
    def emit(self, **kwargs) -> None:
        for callback in self._callbacks:
            cb_obj = callback()
            if cb_obj is not None:
                cb_obj(**kwargs)