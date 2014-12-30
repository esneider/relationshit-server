APP ----> SERVER JSON STRUCTURE:

{
	userId : UUID,
	phoneNumber: #, 
	contactList: [{phone_number : #}, etc.]
	messageList: [{direction : "send"/"receive", time: unix timestamp, phone_number: #, message_len: #}]
}