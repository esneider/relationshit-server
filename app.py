import os
import sys
import json
from flask import Flask, request, Response
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

    print '[start] POST messageList'
    sys.stdout.flush()
    print request.headers
    sys.stdout.flush()

    json = request.get_json(force=True)
    userId = json["userId"]
    messageList = json["messageList"]
    database.upload_messages(userId, messageList)

    print '[end] POST messageList'
    sys.stdout.flush()

    return 'OK'


@app.route('/topLists', methods = ['GET'])
def topLists():

    print '[start] GET topLists'
    sys.stdout.flush()
    print request.headers
    sys.stdout.flush()

    # lists = [('Top friends', [('asd', 123), ('asd', 123)]), ('Top asd', [('asd', 123), ('asd', 123)])]
    userId = request.args.get('IMEI')
    lists = database.process(userId)

    data = json.dumps(lists)
    resp = Response(response=data, mimetype="application/json")

    print '[end] GET topLists'
    sys.stdout.flush()

    return resp


@app.route('/contactsData', methods = ['GET'])
def topLists():

    print '[start] GET contactsData'
    sys.stdout.flush()
    print request.headers
    sys.stdout.flush()

    userId = request.args.get('IMEI')
    blabla = database.user_data(userId)

    data = json.dumps(blabla)
    resp = Response(response=data, mimetype="application/json")

    print '[end] GET contactsData'
    sys.stdout.flush()

    return resp


@app.route('/test')
def api_hello():
    print "before calling process"
    #database.test_query(db)
    #database.contact_query(db, "352584060592000", "32507")
    database.process(db, "352584060592000")
    print "after executing process"
    sys.stdout.flush()

@app.route('/teststats')
def test_stats():
    print "before calling max_unreplied_messages"
    result = database.max_unreplied_messages(db, "352584060592000", "32507")
    print result
    print "after executing max_unreplied_messages"
    sys.stdout.flush()


if __name__ == "__main__":
    app.run(debug=True)
