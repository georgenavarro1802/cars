import sqlite3
from contextlib import contextmanager
from os import path

DATABASE = 'icdb.db'


def _create_database():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("CREATE TABLE cars (Id integer primary key, year integer, make text, model text)")
    c.close()


@contextmanager
def db_cursor():
    """
    Use this as a context manager and it will automatically
    commit and close the database connection for you.
    Example:

        >>> with _db_cursor() as db
        ...     db.execute("SELECT * FROM cars")
        ...     print db.fetchone()
    """
    if not path.exists(DATABASE):
        _create_database()

    conn = sqlite3.connect(DATABASE)
    yield conn.cursor()
    conn.commit()
    conn.close()
