import sqlite3
print("hello")
conn = sqlite3.connect("qqMsg.db")
print("connect database successfully")

sql = 'select qq, msg,Datetime(time,\'localtime\')  from QQMSG'
sql=sql+' where isCar=1 '
sql=sql+' and time>date(\'now\') '
sql=sql+' order by id desc'

print(sql)
cursor = conn.execute(sql)

for row in cursor:
    print("qq->", row[0], "msg-->", row[1], "time->", row[2])

conn.close()
