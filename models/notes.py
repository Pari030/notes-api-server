from typing import List, Union

from models.models import Model, ModelList, Operation


class Note(Model):
    id: int
    text: str

    def __init__(self, _id: int,  text: str):
        super().__init__(_id, text=text)


class Notes(ModelList):

    def __init__(self, name: str = 'notes.db'):
        super().__init__(name)

    @staticmethod
    def note_exists_check(func):
        def wrapper(self, note: Union[Note, int], *args, **kwargs):
            note_id = note if isinstance(note, int) else note.id
            if not self._exists(note_id):
                raise KeyError('Note not found')
            return func(self, note, *args, **kwargs)
        return wrapper

    def create_tables(self):
        self._conn.execute('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, text TEXT)')
        self._conn.commit()

    def add(self, text: str) -> int:
        cur = self._exec('INSERT INTO notes (text) VALUES (?)', (text,), Operation.CURSOR)
        self._conn.commit()
        r = cur.lastrowid
        cur.close()
        return r

    def _exists(self, note_id: int) -> bool:
        row = self._exec('SELECT COUNT(*) FROM notes WHERE id = ?', (note_id,), Operation.FETCHONE)
        return row[0] > 0

    @note_exists_check
    def __getitem__(self, note_id: int):
        r = self._exec('SELECT id, text FROM notes WHERE id = ?', (note_id,), Operation.FETCHONE)
        return Note(*r)

    @note_exists_check
    def __delitem__(self, note_id: int):
        self._exec('DELETE FROM notes WHERE id = ?', (note_id,), Operation.COMMIT)

    @note_exists_check
    def __setitem__(self, note_id: int, note: Note):
        self._exec('UPDATE notes SET text = ? WHERE id = ?', (note.text, note_id), Operation.COMMIT)

    def get_list(self) -> List[Note]:
        return [Note(*r) for r in self._exec('SELECT id, text FROM notes', operation=Operation.CURSOR)]
