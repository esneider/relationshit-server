APP ----> SERVER JSON STRUCTURE:

{
	user_id : UUID,
	phone_number: #, 
	contact_list: [{phone_number : #, name : ""}, etc.]
	message_list: [{direction : "send"/"receive", time: unix timestamp, phone_number: #, message_len: #}]
}