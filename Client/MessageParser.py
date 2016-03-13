import json


class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history

            # Need these if MessageParser is used by the server.
            #'login': self.parse_login,
            #'logout': self.parse_logout,
            #'msg': self.parse_msg,
            #'names': self.parse_names,
            #'help': self.parse_help
        }

    def parse(self, payload):
        payload = json.loads (payload) # decode the JSON object. Save payload as a dict

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            # Response not valid



    def parse_error(self, payload):
        return (payload['timestamp'], payload['sender'], payload['content'])
    
    def parse_info(self, payload):
        return (payload['timestamp'], payload['sender'], payload['content'])
    

    def parse_message(self, payload):
        # message from one client to all the client connected to the server. 'sender' is the client who sent the message
        return (payload['timestamp'], payload['sender'], payload['content'])
    

    def parse_history(self, payload):
        # list of all message responses (as json objects) that the server has previously issued. 'sender' is server
        return (payload['timestamp'], payload['sender'], payload['content'])
    


    #def parse_login(self, payload):
        # if username taken return error. else return a info with a welcome message. Save the usernames in a list. Notify the other users?

    #def parse_logout(self, payload):
        # delete username from list and  return info with a log off message How do I disconnect user?

    #def parse_msg(self, payload):
        # returns a message with msg

    #def parse_names(self, payload):
        # returns info with a list of usernames

    #def parse_help(self, payload):
        # returns info with some help text
