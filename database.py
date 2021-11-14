import inject
import mysql.connector

from config import Config
from contextlib import contextmanager


class Database:
    config = inject.attr(Config)

    @contextmanager
    def connect(self):
        connector = mysql.connector.connect(**self.config.mysql.__dict__)
        try:
            yield connector
        finally:
            connector.close()

    @contextmanager
    def execute(self, query: str, *args):
        with self.connect() as connector:
            with self.execute_with(connector, query, *args) as cursor:
                yield cursor

    @contextmanager
    def execute_with(self, connector, query: str, *args):
        cursor = connector.cursor()
        try:
            cursor.execute(query, args)
            yield cursor
        finally:
            cursor.close()
