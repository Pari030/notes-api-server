import enum
import sqlite3
from typing import List, Union, Any, Optional


class Operation(enum.Enum):
    FETCHALL = 1
    FETCHONE = 2
    COMMIT = 3
    CURSOR = 4


class Model:
    id: int

    def __init__(self, _id: int, **kwargs):
        self.id = _id
        for k, v in kwargs.items():
            setattr(self, k, v)

    def json(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}


class ModelList:
    _conn: Optional[sqlite3.Connection] = None

    def __init__(self, name: str):
        if ModelList._conn is None:
            ModelList._conn = sqlite3.connect(name)

    def _exec(
            self,
            sql: str,
            params: tuple = (),
            operation: Operation = Operation.FETCHONE
    ) -> Union[Any, List[Any], sqlite3.Cursor]:
        cur = self._conn.execute(sql, params)
        r = None
        match operation:
            case Operation.FETCHALL:
                r = cur.fetchall()
            case Operation.FETCHONE:
                r = cur.fetchone()
            case Operation.COMMIT:
                self._conn.commit()
            case Operation.CURSOR:
                r = cur
        if operation != Operation.CURSOR:
            cur.close()
        return r
