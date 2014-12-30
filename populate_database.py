from hello import db
from models import *

def upload_messages(user_id, message_list)
    for message in message_list:
        direction = message["direction"]
        phone_number = message["phone_number"]
        timestamp = message["time"]
        message_len = message["message_len"]
        
        message_obj = Message(user_id, direction, phone_number, timestamp, message_len)
        db.session.add(message_ob) #add message to database
        
        
