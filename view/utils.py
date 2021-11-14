import uuid
from typing import Generic, TypeVar, Hashable

import PySimpleGUI as sg

from event_system import MutableChannel, Channel
from view.constants import APP_NAME, INPUT_DEFAULTS


def init_theme():
    sg.theme("DarkGray13")
    sg.set_options(
        icon="img/icon.ico",
    )


def get_title(title: str):
    return f"{APP_NAME}: {title.title()}"


def hide(window, key: str):
    window[key].update(visible=False)


def set_underline(label: sg.Text, underline=True):
    label.update(font=(
        (*label.Font, 'underline')
        if underline
        else label.Font[:2]
    ))


def auto_id():
    return uuid.uuid4().hex


def join_id(id_: str, *id_parts: str):
    return id_ + '-'.join(id_parts) + '-'


def center(*elements, **kwargs):
    return sg.Column([list(elements)],
                     pad=(0, 0),
                     justification='center', **kwargs)


def layout_from_fields(fields, base_key="-INPUT-", content_kwargs={}):
    description = dict(fields)
    size = (max_len(description.keys())+1, 1)
    font = INPUT_DEFAULTS['font']
    inputs = [
        join_id(base_key, name)
        for name in description
    ]
    layout = [[
            sg.Text(
                label.capitalize().replace('_', ' ') + ':',
                auto_size_text=False,
                font=font,
                size=size,
            ),
            sg.InputText(
                content,
                readonly=True,
                key=input_key,
                **INPUT_DEFAULTS,
                **content_kwargs
            )
        ]
        for (label, content), input_key
        in zip(description.items(), inputs)
    ]
    return layout, inputs


def max_len(iterable):
    return len(max(iterable, key=len))


T = TypeVar("T")


class LiveData(Generic[T]):
    _EVENT = 'LiveDataEvent'

    def __init__(self, value: T = None):
        self._channel: MutableChannel[T] = MutableChannel()
        self._window = None
        self._value: T = None
        if value is not None:
            self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: T):
        self._value = value
        self._channel.publish(self._EVENT, value)

    def observe(self,
                window: sg.Window,
                channel: Channel,
                on_update,
                key: Hashable
                ):
        key = (key, self._EVENT)

        def send_on_update(value: T):
            if window and not window.was_closed():
                window.write_event_value(key, value)

        channel.subscribe(
            key,
            on_update
        )

        self._channel.subscribe(
            self._EVENT,
            send_on_update
        )

        send_on_update(self.value)
