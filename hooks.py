from gunicorn.arbiter import Arbiter

from notes import Notes


def on_starting(_: Arbiter):
    notes = Notes()
    notes.create_tables()
