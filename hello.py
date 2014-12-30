import os
from flask import Flask, request, json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/rebecca')
def second_hello():
    return 'HI!'
@app.route('/miriam')
def third_hello():
    return 'omgggg will you be my friend?'

#def upload_contacts():

@app.route('/messages', methods = ['POST'])
def post():
    user_id = request.json["userId"]
    user_phone_number = request.json["phoneNumber"]
    contact_list = request.json["contactList"]
    message_list = request.json["messageList"]
    #upload_contacts(user_id, contact_list)
    #upload_messages(user_id, message_list)
    #process(contact_list, message_list)
    # send results back

@app.route('/hello')
def api_hello():
    if 'name' in request.args:
        return 'Hello ' + request.args['name']
    else:
        return 'Hello John Doe'
