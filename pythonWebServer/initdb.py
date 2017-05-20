
import sqlite3,os

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect('qqMsg.db')
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    db = connect_db()
    f = open('schema.sql')

    print(f.read())
    db.cursor().executescript(f.read())
    db.commit()
    f.close()
    print("init_db finish")
    cur = db.execute('select qq, msg,isCar from QQMSG order by id desc')
    print(cur)

