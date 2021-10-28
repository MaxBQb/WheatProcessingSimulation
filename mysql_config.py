from dataclasses import dataclass


@dataclass
class MySQLConfig:
    user: str = 'root'
    password: str = ''
    host: str = '127.0.0.1'
    database: str = 'database'
