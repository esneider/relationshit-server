APP ----> SERVER JSON STRUCTURE:

{
	userId : UUID,
	phoneNumber: #, 
	contactList: [{phone_number : #, name : ""}, etc.]
	messageList: [{direction : "send"/"receive", time: unix timestamp, phone_number: #, message_len: #}]
}