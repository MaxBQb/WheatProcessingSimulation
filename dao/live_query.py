from typing import TypeVar, Callable

import inject

from database_observer import DatabaseObserver
from view.livedata import LiveData

T = TypeVar("T")


def live_query(func: Callable[..., T]):
    def wrapper(*args, **kwargs):
        livedata: LiveData[T] = LiveData()
        db_observer = inject.instance(DatabaseObserver)

        def on_update(_):
            livedata.value = func(*args, **kwargs)

        db_observer.subscribe(on_update)
        on_update(None)
        return livedata
    return wrapper
