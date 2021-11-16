from typing import TypeVar, Callable

import inject

from database_observer import DatabaseObserver
from view.livedata import LiveData

T = TypeVar("T")

tables = DatabaseObserver.Event


def live_query(*table_names: str):
    def _live_query(func: Callable[..., T]):
        def wrapper(*args, **kwargs):
            livedata: LiveData[T] = LiveData()
            db_observer = inject.instance(DatabaseObserver)

            def on_update(_):
                livedata.value = func(*args, **kwargs)

            for table in table_names:
                db_observer.channel.subscribe(
                    table, on_update
                )
            on_update(None)
            return livedata
        return wrapper
    return _live_query
