import os
import models
import database
import sys
from flask import Flask, request, json
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/fakemessage', methods = ['POST'])
def fake_message():
    userId = request.json["userId"]
    messageList = request.json["messageList"]
    return repr(messageList)

@app.route('/messages', methods = ['POST'])
def post():
    userId = request.json["userId"]
    # phoneNumber = request.json["phoneNumber"]
    # contactList = request.json["contactList"]
    messageList = request.json["messageList"]
    #upload_contacts(userId, contactList)
    database.upload_messages(db, userId, messageList)
    print "SUCCESS"
    sys.stdout.flush()
    #process(contactList, messageList)
    # send results back

@app.route('/hello')
def api_hello():
    if 'name' in request.args:
        return 'Hello ' + request.args['name']
    else:
        return 'Hello John Doe'
