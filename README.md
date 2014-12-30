### Request JSON Structure

```
{
	userId : UUID,
	phoneNumber: #, 
	contactList: [{phone_number : #}, etc.]
	messageList: [{direction : "send"/"receive", time: unix timestamp, phone_number: #, message_len: #}]
}
```

### Response JSON structure

```
{
	graphs: [
		{ 
			name: "Top Friends"
			data: [
				{ 
					number: 049999999,
					score: 80
				},
				{ 
					number: 0400000000,
					score: 80
				},
			]
		}
	],
	contacts: [
		{
			number: 0499999999,
			score: 50
		}
	]
}
```

