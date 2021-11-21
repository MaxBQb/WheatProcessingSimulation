from typing import Hashable

from event_system import Channel
from view.utils import auto_id, Holder
import PySimpleGUI as sg


class InteractiveRadioButton:
    def __init__(self, values: dict, default: int):
        self.group_key = auto_id()
        self._labels = tuple(values.keys())
        self._values = {
            auto_id(): value
            for value in values.values()
        }
        self.default = tuple(self._values.keys())[default]

    @property
    def radio_buttons(self):
        return [
            sg.Radio(
                label,
                self.group_key,
                key=key,
                default=self.default == key,
                enable_events=True
            ) for label, key in zip(self._labels, self._values.keys())
        ]

    def get_value(self, values: dict):
        for key, value in self._values.items():
            if values[key]:
                return value

    @property
    def keys(self):
        return self._values.keys()

    @classmethod
    def optional_checkbox(cls,
                          on: str,
                          off: str,
                          not_set: str,
                          default: int = -1):
        return cls({
            on: True,
            off: False,
            not_set: None,
        }, default)
