import os
import sqlite3

from flask import request as flask_req
from flask import (Flask, abort, flash, g,  redirect,
                   render_template, session, url_for)

import coolQ_MessagePaser  
import MessageSender  

app = Flask(__name__)

app.config.from_object(__name__)  # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(
    dict(
        DATABASE=os.path.join(app.root_path, 'qqMsg.db'),
        MEMORYDB=False,
        SECRET_KEY='development key',
        USERNAME='admin',
        PASSWORD='default',
        TOKEN='token 987adfv',
        REPLYURL='http://127.0.0.1:5700/'))
app.config.from_envvar('QQMSG_SETTINGS', silent=True)
requestHeaders = {'content-type': 'application/json',
                  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0',
                  'Authorization': app.config['TOKEN']}

msgSender = MessageSender.MsgSender(app.config['REPLYURL'], requestHeaders)
msgPaser = coolQ_MessagePaser.MessagePaser(msgSender)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

#globalDB  = connect_db()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """

    #return globalDB
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            print(f.read())
            db.cursor().executescript(f.read())
        db.commit()
        print("init_db finish")


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def checkToken():
    if flask_req.headers["Authorization"] == app.config['TOKEN']:
        return True
    return False


def isNeedGroup(group_id):
    if group_id == 227869724:
        return True
    if group_id == 273371109:
        return True
    return False


def publishCars(data):
    db = get_db()
    db.execute('insert into QQMSG (qq,QQGROUP,msg,isCar) values (?,?,?,?)',
               [data.get('user_id'), data.get('group_id'), data.get('message'), 1])
    db.commit()


def publishFindCar(data):
    db = get_db()
    db.execute('insert into QQMSG (qq,QQGROUP,msg,isCar) values (?,?,?,?)',
               [data.get('user_id'), data.get('group_id'), data.get('message'), 0])
    db.commit()


def getCars(group_id=''):
    db = get_db()
    sql = 'select qq, msg,Datetime(time,\'localtime\')  from QQMSG where isCar=1'
    if group_id != '':
        sql = sql + ' and QQGROUP=' + str(group_id)
        
    sql=sql+' and time>date(\'now\') '
    sql = sql + ' order by id desc'
    #print(sql)
    cur = db.execute(sql)
    s = ''
    for row in cur:
        s = s + "\n" + "[" + str(row[2]) + "]" + \
            " QQ:" + str(row[0]) + "-->" + str(row[1])
    return s


def passMessage_Group(data):
    if isNeedGroup(data.get('group_id')) is False:
        return '', 204
    if msgPaser.isCar(data) == True:
        publishCars(data)
        return '', 204
    if msgPaser.isFindCar(data) == True:
        cars = getCars(data.get('group_id'))
        if len(cars) > 0:
            msgSender.send_private_msg(data.get('user_id'),  "reply:" + cars)
        publishFindCar(data)
        return '', 204

    return msgPaser.isAdminMsg(data)


@app.route('/', methods=['GET'])
def indexGet():
    shtml = "<h1> <a href='/login'>login.</a></h1>"
    shtml = shtml + "<br><h1> <a href='/show'>show.</a></h1>"
    return shtml


@app.route('/', methods=['POST'])
def index():
    if checkToken() is False:
        return '', 500
    data = flask_req.json or {}
    if data.get('post_type') == 'message':
        if data.get('message_type') == 'private':
            return msgPaser.passMessage_Private(data)
        elif data.get('message_type') == 'group':
            return passMessage_Group(data)
    return '', 204


@app.route('/show')
def show_entries():
    db = get_db()
    cur = db.execute(
        'select qq, msg,isCar,Datetime(time,\'localtime\')  from QQMSG order by id desc')
    entries = [dict(title=row[0], text=row[1], isCar=row[2], time=row[3])
               for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into QQMSG (QQ,QQGROUP, msg) values (?,?, ?)',
               [flask_req.form['title'], 00, flask_req.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if flask_req.method == 'POST':
        if flask_req.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif flask_req.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    if app.config['MEMORYDB']:
        app.config['DATABASE'] = ':memory:'
        init_db()

    app.run(host='0.0.0.0', port=8888, debug=False)
