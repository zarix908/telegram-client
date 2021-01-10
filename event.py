from typing import TypeVar, Callable, Set, Generic

T = TypeVar('T', bound=Callable[..., None])


class Event(Generic[T]):
    def __init__(self):
        self.__listeners: Set[T] = set()

    def __call__(self, *args, **kwargs) -> None:
        for listener in self.__listeners:
            listener(*args, **kwargs)

    def __iadd__(self, listener: T):
        self.__listeners.add(listener)
        return self

    def __isub__(self, listener: T):
        self.__listeners.remove(listener)
        return self
