import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/rebecca')
def second_hello():
    return 'HI!'
@app.route('/miriam')
def second_hello():
    return 'hello will you be my friend?'
