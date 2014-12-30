import models

def upload_messages(db, userId, messageList):
    for message in messageList:
        direction = message["direction"]
        phoneNumber = message["phoneNmber"]
        timestamp = message["timestamp"]
        messageLength = message["messageLength"]

        message_obj = models.Message(1, userId, direction, phoneNumber, timestamp, messageLength)
        db.session.add(message_obj) #add message to database
    db.session.commit()

def upload_contacts(db, userId, contactList):
	for contact in contactList:
        userId = userId
        phoneNumber = contact["phoneNumber"]
        contactType = contact["contactType"]

        contact_obj = models.Contacts(1, userID, phoneNumber, contactType)
      	db.session.add(contact_obj)
    db.session.commit()

def process():
	pass
