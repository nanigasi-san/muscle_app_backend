import sqlite3
import os

from models import Training


class MyCursur(sqlite3.Cursor):
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        super().__init__(self.conn)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
        self.conn.commit()
        self.conn.close()


DB_PATH = "db.sqlite3"


def reset_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    with MyCursur(DB_PATH) as cur:
        cur.execute("CREATE TABLE TRAINING (name text)")


def add_training(training: Training):
    with MyCursur(DB_PATH) as cur:
        cur.execute("INSERT INTO TRAINING VALUES (?)", (training.name, ))


def list_training():
    with MyCursur(DB_PATH) as cur:
        cur.execute("SELECT * FROM TRAINING")
        return cur.fetchall()


reset_db()
t = Training(name="unnko")
add_training(t)
print(list_training())
