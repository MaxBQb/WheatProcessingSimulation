from threading import Thread
from time import sleep

import inject

from config import Config
from dao.changes import ChangesDAO
from event_system import MutableChannel, Channel


class DatabaseObserver:
    source = inject.attr(ChangesDAO)
    config = inject.attr(Config)

    def __init__(self):
        self._channel: MutableChannel[None] = MutableChannel()
        self._last_change = None
        self._force_update = True
        self._thread = Thread(
            name="DatabasePolling",
            target=self._poll_db,
            daemon=True
        )
        self._UPDATE_EVENT = 0

    def subscribe(self, *callbacks: Channel.Callback):
        self._channel.subscribe(self._UPDATE_EVENT, *callbacks)

    def run(self):
        self._thread.start()

    def _poll_db(self):
        while True:
            try:
                if self._force_update or self._has_changes():
                    self._channel.publish(self._UPDATE_EVENT, None)
                    self._force_update = False
            except Exception as e:
                self._force_update = True
                print(e)
            sleep(self.config.database_observer.refresh_interval)

    def _has_changes(self):
        last_change = self.source.get_last_change()
        if not last_change:
            return False
        last_change = last_change.timestamp()
        if last_change != self._last_change:
            self._last_change = last_change
            return True
        return False
