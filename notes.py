import sqlite3


class Notes:

    _conn: sqlite3.Connection

    def __init__(self):
        self._conn = sqlite3.connect('notes.db')

    def create_tables(self):
        self._conn.execute('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, text TEXT)')
        self._conn.commit()

    def add(self, text: str) -> int:
        cur = self._conn.execute('INSERT INTO notes (text) VALUES (?)', (text,))
        self._conn.commit()
        r = cur.lastrowid
        cur.close()
        return r

    def _exists(self, note_id: int) -> bool:
        cur = self._conn.execute('SELECT COUNT(*) FROM notes WHERE id = ?', (note_id,))
        r = cur.fetchone()[0] > 0
        cur.close()
        return r

    def __getitem__(self, note_id: int):
        if not isinstance(note_id, int):
            raise TypeError('Note id must be an integer')
        if not self._exists(note_id):
            raise KeyError('Note not found')
        cur = self._conn.execute('SELECT text FROM notes WHERE id = ?', (note_id,))
        r = cur.fetchone()[0]
        cur.close()
        return r

    def __delitem__(self, note_id: int):
        if not isinstance(note_id, int):
            raise TypeError('Note id must be an integer')
        if not self._exists(note_id):
            raise KeyError('Note not found')
        self._conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        self._conn.commit()

    def __setitem__(self, note_id: int, text: str):
        if not isinstance(note_id, int):
            raise TypeError('Note id must be an integer')
        if not self._exists(note_id):
            raise KeyError('Note not found')
        self._conn.execute('UPDATE notes SET text = ? WHERE id = ?', (text, note_id))
        self._conn.commit()

    def get_list(self) -> list:
        cur = self._conn.execute('SELECT id, text FROM notes')
        return cur.fetchall()
