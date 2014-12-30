from app import db

class Message(db.Model):
	__tablename__ = 'Messages'
    user_id = db.Column(db.Integer, primary_key = True)
    direction = db.Column(db.String(80), nullable = False) # either 'send' or 'receive'
    phone_number = db.Column(db.String(120), nullable = False)
    timestamp = db.Column(db.DateTime, nullable = False, timezone = True) # make it timezone aware?
    message_len = db.Column(db.Integer)    

    def __init__(self, user_id, direction, phone_number, timestamp, message_len):
	    self.user_id = user_id
	    self.direction = direction
	    self.phone_number = phone_number
	    self.timestamp = timestamp
	    self.message_len = message_len

    def __repr__(self):
        return '' # alter later

class Contacts(db.Model):
	__tablename__ = 'Contacts'
	user_id = db.Column(db.Integer, primary_key = True)
	contact_name = db.Column(db.String(120), nullable = False)
	contact_phone_number = db.Column(db.String(120), nullable = False)

	def __init__(self, user_id, contact_name, contact_phone_number):
		self.user_id = user_id
		self.contact_name = contact_name 
		self.contact_phone_number = contact_phone_number