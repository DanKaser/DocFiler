from __future__ import annotations
from sqlalchemy import create_engine, Text as sa_text, Connection
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

_SQLITE_PRAGMA = sa_text('PRAGMA foreign_keys = ON;')

def setup_db_con(path: str, base: DeclarativeBase) -> None:

    DBConnSingleton.set_path(path)
    DBConnSingleton.set_base(base)

class MissingParameterError(Exception):

    def __init__(self, msg: str) -> None:
        super().__init__(msg)

class DBConnSingleton:

    _instance: DBConnSingleton|None = None
    _initialized: bool = False
    _path: str|None = None
    _base: DeclarativeBase|None = None

    @classmethod
    def set_path(cls, path: str) -> None:
        cls._path = path

    @classmethod
    def set_base(cls, base: DeclarativeBase) -> None:
        cls._base = base

    def __new__(cls, **kwargs) -> DBConnSingleton:
        if cls._instance is None:
            if not (cls._path or cls._base):
                raise MissingParameterError('DB path or Base must be set for initialization')
            cls._instance = super().__new__(cls)
            return cls._instance
        else: return cls._instance

    def __init__(self, **kwargs) -> None:
        """Accepts connection_args using kwargs"""
        if not self._initialized:
            self._engine = create_engine(f'sqlite:///{self._path}', **kwargs)
            self._sessionmaker = sessionmaker(bind = self._engine)
            self.create_tables()
            self._initialized = True

    def get_session(self) -> Session:
        s = self._sessionmaker()
        s.execute(_SQLITE_PRAGMA)
        return s

    def get_connection(self) -> Connection:
        conn = self.engine.connect()
        conn.exec_driver_sql(_SQLITE_PRAGMA)
        return conn

    def create_tables(self) -> None:
        self._base.metadata.create_all(self._engine)
