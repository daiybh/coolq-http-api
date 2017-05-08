from flask import Flask,jsonify

app = Flask(__name__)

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


@app.route("/")
def index():
    #return "<h1>Hello world!</h1>"
    response = Flask.make_response('<h1>hello world! response</h1>',200)
    response.set_cookie('answer','42')
    
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8887)