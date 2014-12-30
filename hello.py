import os
from flask import Flask, request, json

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/rebecca')
def second_hello():
    return 'HI!'
@app.route('/miriam')
def third_hello():
    return 'omgggg will you be my friend?'


@app.route('/post', methods = ['POST'])
def post():
    return "JSON Message: " + json.dumps(request.json)

@app.route('/hello')
def api_hello():
    if 'name' in request.args:
        return 'Hello ' + request.args['name']
    else:
        return 'Hello John Doe'
