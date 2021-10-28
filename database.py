import inject
import mysql.connector

from config import Config
from contextlib import contextmanager


class Database:
    config = inject.attr(Config)

    def __init__(self):
        self._connector = mysql.connector.connect(
            **self.config.mysql.__dict__
        )

    @contextmanager
    def execute(self, query: str, *args):
        cursor = self._connector.cursor()
        cursor.execute(query, args)
        yield cursor
        cursor.close()


