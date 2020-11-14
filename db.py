import sqlite3
import os
from datetime import date
from random import choice
from models import Training, Task


def gen_id():
    table = "abcdefghijklmnopqrstuvwxyz"
    id = ""
    for i in range(10):
        id += choice(table)
    return id


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
        cur.execute("CREATE TABLE TASK (\
                    name text,\
                    load int,\
                    number int,\
                    task_date text,\
                    done int,\
                    id int\
                    )")


def add_training(training: Training):
    with MyCursur(DB_PATH) as cur:
        cur.execute("INSERT INTO TRAINING VALUES (?)", (training.name, ))


def list_training():
    with MyCursur(DB_PATH) as cur:
        cur.execute("SELECT * FROM TRAINING")
        return cur.fetchall()


def add_task(task: Task):
    with MyCursur(DB_PATH) as cur:
        cur.execute("INSERT INTO TASK VALUES (?, ?, ?, ?, ?, ?)", (task.name, task.load, task.number, None, int(False), gen_id()))


def list_done_task():
    with MyCursur(DB_PATH) as cur:
        cur.execute("SELECT * FROM TASK WHERE done=1")
        return cur.fetchall()


def list_undone_task():
    with MyCursur(DB_PATH) as cur:
        cur.execute("SELECT * FROM TASK WHERE done=0")
        return cur.fetchall()


reset_db()
tr = Training(name="unnko")
add_training(tr)
print(list_training())

ta1 = Task(name="unnko", load=85, number=30)
add_task(ta1)
ta2 = Task(name="tinko", load=120, number=30)
add_task(ta2)
print(list_done_task())
print(list_undone_task())
