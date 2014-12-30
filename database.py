import models

def upload_messages(db, userId, messageList):
    for message in messageList:
        direction = message["direction"]
        phoneNumber = message["phoneNumber"]
        timestamp = message["timestamp"]
        messageLength = message["messageLength"]

        message_obj = models.Message(1, userId, direction, phoneNumber, timestamp, messageLength)
        db.session.add(message_obj) #add message to database
