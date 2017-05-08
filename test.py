import requests
from flask import Flask,jsonify,make_response
from flask import request as flask_req

app = Flask(__name__)

def send_msg(func,jsonMsg):
    requests.post('http://127.0.0.1:5700/'+func, json=jsonMsg)
def send_private_msg(jsonMsg):
    send_msg('send_private_msg', jsonMsg)

def send_private_msg(jsonMsg):
    send_msg('send_private_msg', jsonMsg)
    
def passMessage_Group(data):
    if data.get('user_id')==7277017:
        return jsonify({
                'user_id': data.get('user_id'),
                'reply': data.get('message')
            })
    return '',204


def passMessage_Private(data):
    jsonMsg = {
                'user_id': data.get('user_id'),
                'message': data.get('message')
            }
    send_private_msg(jsonMsg)
    return '',204

@app.route('/')
def index_main():
    #return '<h1>hello world!</h1>'
    response = Flask.make_response('<h1>hello world!</h1>',200)
    response.set_cookie('answer','42')    
    return response


@app.route('/', methods=['POST'])
def index():
    data = flask_req.json or {}
    if data.get('post_type') == 'message':
        if data.get('message_type') == 'private':
            return passMessage_Private(data)  
        elif data.get('message_type') == 'group':
            return passMessage_Group(data)
    return  '',204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
