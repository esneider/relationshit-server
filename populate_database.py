from models import *

def upload_messages(db, userId, messageList):
    for message in messageList:
        direction = message["direction"]
        phoneNumber = message["phoneNmber"]
        timestamp = message["timestamp"]
        messageLength = message["messageLength"]

        message_obj = Message(userId, direction, phoneNumber, timestamp, messageLength)
        db.session.add(message_obj) #add message to database
