import json


class MessageParser():
	def __init__(self):
		
		self.possible_responses = {
			'error': self.parse_error,
			'info': self.parse_info,
			'message': self.parse_message,
			'history': self.parse_history
		}

	def parse(self, payload):
		payload = json.loads (payload) # decode the JSON object. Save payload as a dict
		
		if payload['response'].lower() in self.possible_responses:
			return self.possible_responses[payload['response'].lower()](payload)
		else:
			# Response not valid
			return None, None, None, None
		
		
	def parse_error(self, payload):
		return (payload['response'], payload['timestamp'], payload['sender'], payload['content'])
		
	def parse_info(self, payload):
		return (payload['response'], payload['timestamp'], payload['sender'], payload['content'])
		
		
	def parse_message(self, payload):
		# message from one client to all the client connected to the server. 'sender' is the client who sent the message
		return (payload['response'], payload['timestamp'], payload['sender'], payload['content'])
		
		
	def parse_history(self, payload):
		# list of all message responses (as json objects) that the server has previously issued. 'sender' is server
		return (payload['response'], payload['timestamp'], payload['sender'], payload['content'])
