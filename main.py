import traceback

from flask import Flask

import utils
from models.notes import Notes, Note

app = Flask(__name__)


@app.route('/notes', methods=['GET'])
def get_notes():
    notes = Notes()
    return [note.json() for note in notes.get_list()]


@app.get('/notes/<int:note_id>')
def get_note(note_id: int):
    notes = Notes()
    note = notes[note_id]
    return note.json()


@app.post('/notes')
def create_note():
    notes = Notes()
    text = utils.get_param('text')
    notes.add(text)
    return '', 201


@app.put('/notes/<int:note_id>')
def update_note(note_id: int):
    notes = Notes()
    text = utils.get_param('text')
    notes[note_id] = Note(note_id, text)
    return '', 200


@app.delete('/notes/<int:note_id>')
def delete_note(note_id: int):
    notes = Notes()
    del notes[note_id]
    return '', 200


@app.errorhandler(KeyError)
def handle_key_error(e):
    return {'error': str(e)}, 404


@app.errorhandler(TypeError)
def handle_type_error(e):
    traceback.print_exc()
    return {'error': str(e)}, 400


@app.errorhandler(ValueError)
def handle_value_error(e):
    traceback.print_exc()
    return {'error': str(e)}, 400


if __name__ == '__main__':
    Notes().create_tables()
    app.run(debug=True)
