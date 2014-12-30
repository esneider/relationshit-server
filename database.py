import sys
import models
from app import db


def upload_messages(userId, messageList):

    NUM_TOP_FRIENDS = 10

    for message in messageList:
        direction     = message["direction"]
        phoneNumber   = message["phoneNumber"]
        timestamp     = message["timestamp"]
        messageLength = message["messageLength"]

        message_obj = models.Message(userId, direction, phoneNumber, timestamp, messageLength)
        db.session.add(message_obj)

    db.session.commit()


def upload_contacts(userId, contactList):

    for contact in contactList:
        phoneNumber = contact["phoneNumber"]
        contactType = contact["contactType"]

        contact_obj = models.Contacts(userId, phoneNumber, contactType)
        db.session.add(contact_obj)

    db.session.commit()

def process(db, userId):
    create_graphs(db, userId)
    pass

def create_graphs(db, userId):
    pass
