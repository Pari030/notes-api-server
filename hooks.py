from gunicorn.arbiter import Arbiter

from models.notes import Notes


def on_starting(_: Arbiter):
    notes = Notes()
    notes.create_tables()
