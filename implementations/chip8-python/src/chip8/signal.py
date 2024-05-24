from typing import Any, Callable
import weakref


class Signal:
    _callbacks: list[weakref.ref | Callable]

    def __init__(self) -> None:
        self._callbacks = []

    def connect(self, fn: Callable[..., Any]) -> Callable[..., Any]:
        self._callbacks.append(fn)
        return fn

    def connect_fn(self, callback: Callable[..., Any]) -> None:
        self._callbacks.append(weakref.ref(callback))

    def emit(self, **kwargs) -> None:
        for callback in self._callbacks:
            if isinstance(callback, weakref.ref):
                cb_obj = callback()
                if cb_obj is not None:
                    cb_obj(**kwargs)
            else:
                callback(**kwargs)
