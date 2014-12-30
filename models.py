from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Message(db.Model):
    __tablename__ = 'Messages'

    userId = db.Column(db.Integer, nullable = False)     # add foreign key
    direction = db.Column(db.String(80), nullable = False)     # either 'send' or 'receive'
    phoneNumber = db.Column(db.String(120), nullable = False)
    timestamp = db.Column(db.Integer, nullable = False)
    messageLength = db.Column(db.Integer, nullable = False)

    def __init__(self, userId, direction, phoneNumber, timestamp, messageLength):
        self.userId = userId
        self.direction = direction
        self.phoneNumber = phoneNumber
        self.timestamp = timestamp
        self.messageLength = messageLength

class Contacts(db.Model):
    __tablename__ = 'Contacts'

    userId = db.Column(db.Integer, nullable = False)
    phoneNumber = db.Column(db.String(120), nullable = False)
    contactType = db.Column(db.String(120), nullable = False)     # default is "regular"

    def __init__(self, userId, phoneNumber, contactType):
        self.userId = userId
        self.phoneNumber = phoneNumber
        self.contactType = contactType
