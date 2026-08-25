"""
Database setup. Plain SQLite via SQLAlchemy - no server, no auth,
just a single file (mahila_mitra.db) created next to app.py.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)
    with app.app_context():
        # Importing here (not at module top) avoids a circular import
        # between database.py and models.py.
        from models import MoodResult  # noqa: F401
        db.create_all()
