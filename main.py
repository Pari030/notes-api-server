from flask import Flask, request

from notes import Notes

app = Flask(__name__)


@app.route('/notes', methods=['GET'])
def get_notes():
    notes = Notes()
    return [{'id': note_id, 'text': text} for note_id, text in notes.get_list()]


@app.get('/notes/<int:note_id>')
def get_note(note_id):
    notes = Notes()
    return {'id': note_id, 'text': notes[note_id]}


@app.post('/notes')
def create_note():
    notes = Notes()
    try:
        text = request.json['text']
    except KeyError:
        return {'error': 'Missing note text'}, 400

    notes.add(text)
    return '', 201


@app.put('/notes/<int:note_id>')
def update_note(note_id: int):
    notes = Notes()
    try:
        text = request.json['text']
    except KeyError:
        return {'error': 'Missing note text'}, 400
    notes[note_id] = text
    return '', 200


@app.delete('/notes/<int:note_id>')
def delete_note(note_id):
    notes = Notes()
    del notes[note_id]
    return '', 200


@app.errorhandler(KeyError)
def handle_key_error(e):
    return {'error': str(e)}, 404


@app.errorhandler(TypeError)
def handle_type_error(e):
    return {'error': str(e)}, 400


if __name__ == '__main__':
    app.run(debug=True)
