from twilio.rest import Client


accound_sid="AC7a811a08c6ca0e18b0d157e1dfacd33f"
auth_token="8f998f952bab33ca0d4c54703c1bb669"
twilio_number="+15104803663"

client=Client(accound_sid,auth_token)

def sms(phn_nbr):
	client.messages.create(
		body='test sms',
		from_=twilio_number,
		to=phn_nbr
		)

sms("+8801623708711")