import os
import sys
from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

import database


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/fakemessage', methods = ['POST'])
def fake_message():
    userId = request.json["userId"]
    messageList = request.json["messageList"]
    return messageList


@app.route('/messageList', methods = ['POST'])
def messageList():
    userId = request.json["userId"]
    # phoneNumber = request.json["phoneNumber"]
    messageList = request.json["messageList"]
    database.upload_messages(userId, messageList)
    # process(contactList, messageList)
    # send results back
    return 'SUCCESS'


@app.route('/hello')
def api_hello():
    if 'name' in request.args:
        return 'Hello ' + request.args['name']
    else:
        return 'Hello John Doe'
