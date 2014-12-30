from hello import db

class Message(db.Model):
	__tablename__ = 'Messages'
    userId = db.Column(db.Integer, nullable = False) # add foreign key
    direction = db.Column(db.String(80), nullable = False) # either 'send' or 'receive'
    phoneNumber = db.Column(db.String(120), nullable = False)
    timestamp = db.Column(db.TIMESTAMP, nullable = False)
    messageLength = db.Column(db.Integer, nullable = False)    

    def __init__(self, user_id, direction, phone_number, timestamp, message_len):
	    self.userId = user_id
	    self.direction = direction
	    self.phoneNumber = phone_number
	    self.timestamp = timestamp
	    self.messageLength = message_len

class Contacts(db.Model):
	__tablename__ = 'Contacts'
	userId = db.Column(db.Integer, nullable = False)
	phoneNumber = db.Column(db.String(120), nullable = False)
	contactType = db.Column(db.String(120), nullable = False) # default = "regular"

	def __init__(self, user_id, contact_phone_number, contact_type):
		self.userId = user_id
		self.phoneNumber = contact_phone_number
		self.contactType = contact_type