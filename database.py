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
    def cursor(self, commit_changes=False):
        with self.connect() as connector:
            cursor = connector.cursor()
            try:
                yield cursor
                if commit_changes:
                    connector.commit()
            finally:
                cursor.close()

    @contextmanager
    def execute(self, query: str, *args, commit_changes=False):
        with self.cursor(commit_changes) as cursor:
            cursor.execute(query, args)
            yield cursor
