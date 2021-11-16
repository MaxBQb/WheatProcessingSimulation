import inject

from database_observer import DatabaseObserver
from view.livedata import LiveData


tables = DatabaseObserver.Event


def live_query(*tables: str):
    def _live_query(func):
        def wrapper(*args, **kwargs):
            livedata = LiveData()
            db_observer = inject.instance(DatabaseObserver)

            def on_update(_):
                livedata.value = func(*args, **kwargs)

            for table in tables:
                db_observer.channel.subscribe(
                    table, on_update
                )
            on_update(None)
            return livedata
        return wrapper
    return _live_query
