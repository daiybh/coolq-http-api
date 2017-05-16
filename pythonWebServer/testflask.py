#from flask import Flask,jsonify,g
import sqlite3,os,random
from flask import Flask, g
app = Flask(__name__)
print("111111")
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

bInited=False
def ConnectDB():
    con = sqlite3.connect(':memory:')
    return con

mydb=ConnectDB()

def getdb():
    
    print("mydb",mydb)
    return mydb
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = ConnectDB()
    return g.sqlite_db

def InitDB():
    db = mydb
    # 创建a,b,c三个字段
    db.cursor().execute('create table test (a char(256), b char(256), c char(256));')
    # 为字段a,b创建索引
    db.cursor().execute('create index a_index on test(a)')
    db.cursor().execute('create index b_index on test(b)')
    # 插入一条数据
    db.cursor().execute('insert into test values(?, ?, ?)', (-1,0,1))
    # 查询符合特定要求的数据
    #cur.execute('select * from test where a=? and b=?',(-1, 0))
    
@app.route("/add")
def add():
    #return "<h1>Hello world!</h1>"
    db = getdb()

    db.cursor().execute('insert into test values(?,?,?)', (random.randint(12, 20) ,888,88))
    #entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    sHtml='<table>'
    db.commit()

    return index()

@app.route("/")
def index():
    #return "<h1>Hello world!</h1>"
    db = getdb()

    cur = db.execute('select * from test ')
    #entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    sHtml='<table>'
    data = cur.fetchall()

    for e in data:
        sHtml+='<tr><td>'+str(e)+'</td></tr>'
    sHtml+='</table>'
    return sHtml,200
print("22222")

if __name__ == '__main__':
    InitDB()
    app.run(host='0.0.0.0', port=8887)
