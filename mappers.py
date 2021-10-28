import re
from typing import Iterable

_pascal_case_pattern = re.compile('(.)([A-Z][a-z]+)')
_camel_case_pattern = re.compile('([a-z0-9])([A-Z])')


def _to_snake_case(text):
    name = _pascal_case_pattern.sub(r'\1_\2', text)
    return _camel_case_pattern.sub(r'\1_\2', text).lower()


def _field_name(base_name: str, clazz: type):
    names = set(clazz.__annotations__)
    class_name = _to_snake_case(clazz.__name__)
    modifiers = (
        lambda x: x,
        _to_snake_case,
        lambda x: (
            x.removeprefix(class_name+'_')
            if x.startswith(class_name)
            else x
        ),
        lambda x: class_name + '_' + x,
    )
    for modifier in modifiers:
        base_name = modifier(base_name)
        if base_name in names:
            return base_name


def table_to_model(keys: Iterable, values: Iterable, clazz: type):
    return clazz(**{
        _field_name(key, clazz): value
        for key, value in zip(keys, values)
    })
