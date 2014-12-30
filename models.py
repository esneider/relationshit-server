import sys
from app import db


class Message(db.Model):
    __tablename__ = 'messages'

    id            = db.Column(db.Integer, nullable = False, primary_key = True)
    userId        = db.Column(db.String(256), nullable = False)
    direction     = db.Column(db.String(256), nullable = False)  # Either 'send' or 'receive'
    phoneNumber   = db.Column(db.String(256), nullable = False)
    timestamp     = db.Column(db.String(256), nullable = False)
    messageLength = db.Column(db.Integer, nullable = False)

    def __init__(self, userId, direction, phoneNumber, timestamp, messageLength):
        self.userId        = userId
        self.direction     = direction
        self.phoneNumber   = phoneNumber
        self.timestamp     = str(timestamp)
        self.messageLength = messageLength


class Contacts(db.Model):
    __tablename__ = 'contacts'

    id          = db.Column(db.Integer, nullable = False, primary_key = True)
    userId      = db.Column(db.String(256), nullable = False)
    phoneNumber = db.Column(db.String(256), nullable = False)
    contactType = db.Column(db.String(256), nullable = False)     # default is "regular"

    def __init__(self, userId, phoneNumber, contactType):
        self.userId      = userId
        self.phoneNumber = phoneNumber
        self.contactType = contactType
