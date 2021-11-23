from typing import TypeVar, Generic, Hashable, Callable
import PySimpleGUI as sg
from event_system import MutableChannel, Channel


T = TypeVar("T")


class LiveData(Generic[T]):
    _EVENT = 'LiveDataEvent'

    def __init__(self, value: T = None):
        self._channel: MutableChannel[T] = MutableChannel()
        self._value: T = None
        self._transformations = []
        if value is not None:
            self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: T):
        for func in self._transformations:
            value = func(value)
        if self._value == value:
            return
        self._value = value
        self._channel.publish(self._EVENT, value)

    def observe(self,
                window: sg.Window,
                channel: Channel,
                on_update,
                key: Hashable):
        key = (key, self._EVENT)

        def stop_observation():
            self._channel.unsubscribe(
                self._EVENT,
                send_on_update
            )
            channel.unsubscribe(key, on_update)

        def send_on_update(value: T):
            if window and not window.was_closed():
                window.write_event_value(key, value)
            else:
                stop_observation()

        channel.subscribe(key, on_update)
        self._channel.subscribe(
            self._EVENT,
            send_on_update
        )
        send_on_update(self.value)
        return stop_observation

    def map(self, transformation: Callable):
        self._transformations.append(transformation)
        self._value = transformation(self._value)
        self._channel.publish(self._EVENT, self._value)
        return self
