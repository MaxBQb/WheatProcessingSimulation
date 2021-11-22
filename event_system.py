from typing import Callable, Hashable, TypeVar, Generic

T = TypeVar('T')


class Channel(Generic[T]):
    Callback = Callable[[T], None]

    def __init__(self):
        self._events_map: dict[Hashable, list[Channel.Callback]] = {}

    def subscribe_foreach(self, events: tuple, *callbacks: Callback):
        for event in events:
            self.subscribe(event, *callbacks)

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


class ChannelRouter:
    def __init__(self):
        self._category_map: dict[Hashable, MutableChannel] = {}

    def subscribe(self, category: Hashable, channel: MutableChannel):
        self._category_map.setdefault(category, channel)

    def unsubscribe(self, category: Hashable):
        del self._category_map[category]


class MutableChannelRouter(ChannelRouter):
    def publish(self, category: Hashable, event: Hashable, value):
        channel = self._category_map.get(category, None)
        if not channel:
            return
        channel.publish(event, value)

    def broadcast(self, event: Hashable, value):
        for category in self._category_map:
            self.publish(category, event, value)
