from typing import Callable, Hashable, TypeVar, Generic

T = TypeVar('T')


class Channel(Generic[T]):
    Callback = Callable[[T], None]

    def __init__(self):
        self._events_map: dict[Hashable, list[Channel.Callback]] = {}

    def subscribe(self, event: Hashable, *callbacks: Callback):
        self._events_map.setdefault(event, [])
        self._events_map[event] += list(callbacks)

    def unsubscribe(self, event: Hashable, *callbacks: Callback):
        if event not in self._events_map:
            return

        for callback in callbacks:
            self._events_map[event].remove(callback)


class MutableChannel(Channel[T]):
    _NO_CALLBACKS = tuple()

    def publish(self, event: Hashable, value: T):
        callbacks = self._events_map.get(event, self._NO_CALLBACKS)
        for callback in callbacks:
            callback(value)
