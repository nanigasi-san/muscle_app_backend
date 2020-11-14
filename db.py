import sqlite3
import os
from datetime import date
from random import choice
from models import Training, Task, TaskId


def gen_id():
    table = "abcdefghijklmnopqrstuvwxyz"
    id = ""
    for i in range(10):
        id += choice(table)
    return id


def execute_sql(sql, args=tuple()):
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute(sql, args)
        conn.commit()
        return cur.fetchall()


DB = "db.sqlite3"


def reset_db():
    if os.path.exists(DB):
        os.remove(DB)
    execute_sql("CREATE TABLE TRAINING (name text)")
    execute_sql("CREATE TABLE TASK (\
                    name text,\
                    load int,\
                    number int,\
                    task_date text,\
                    done int,\
                    id int\
                    )")


def add_training(training: Training):
    execute_sql("INSERT INTO TRAINING VALUES (?)", (training.name, ))


def list_training():
    return execute_sql("SELECT * FROM TRAINING")


def add_task(task: Task):
    execute_sql("INSERT INTO TASK VALUES (?, ?, ?, ?, ?, ?)", (task.name, task.load, task.number, None, int(False), gen_id()))


def mark_task_as_done(task_id: TaskId):
    execute_sql("UPDATE TASK SET done=? , task_date=? WHERE id=?", (int(True), date.today().strftime("%Y/%m/%d"), task_id))


def list_done_task():
    return execute_sql("SELECT * FROM TASK WHERE done=1")


def list_undone_task():
    return execute_sql("SELECT * FROM TASK WHERE done=0")


reset_db()
tr = Training(name="unnko")
add_training(tr)
print(list_training())

ta1 = Task(name="unnko", load=85, number=30)
add_task(ta1)
ta2 = Task(name="tinko", load=120, number=30)
add_task(ta2)
mark_task_as_done("hogehogeid")
print(list_done_task())
print(list_undone_task())
