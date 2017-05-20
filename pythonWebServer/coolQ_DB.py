import sqlite3
import os
print("hello")
conn = sqlite3.connect("qqMsg.db")
print("connect database successfully")
cursor = conn.execute(
    'select qq, msg,Datetime(time,\'localtime\')  from QQMSG where isCar=1 order by id desc')

for row in cursor:
    print("qq->", row[0], "msg-->", row[1], "time->", row[2])

conn.close()
