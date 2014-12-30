import os
from flask import Flask, request

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


@app.route('/post')
def post():
    # Get the parsed contents of the form data
    json = request.json
    print(json)
    # Render template
    return json

@app.route('/hello')
def api_hello():
    if 'name' in request.args:
        return 'Hello ' + request.args['name']
    else:
        return 'Hello John Doe'
