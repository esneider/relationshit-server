from models import *

def upload_messages(db, user_id, message_list):
    for message in message_list:
        direction = message["direction"]
        phone_number = message["phoneNmber"]
        timestamp = message["timestamp"]
        message_len = message["messageLength"]
        
        message_obj = Message(user_id, direction, phone_number, timestamp, message_len)
        db.session.add(message_obj) #add message to database
        
