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

@app.route('/messages', methods = ['POST'])
def post():
    userId = request.json["userId"]
    # phoneNumber = request.json["phoneNumber"]
    # contactList = request.json["contactList"]
    messageList = request.json["messageList"]
    # upload_contacts(userId, contactList)
    database.upload_messages(userId, messageList)
    # process(contactList, messageList)
    # send results back
    return 'SUCCESS'


@app.route('/test')
def api_hello():
    print "before calling process"
    database.process(db, userId)
    print "after executing process"