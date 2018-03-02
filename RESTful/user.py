class User:
    def __init__(self, _id, username, password):   ## used _ before id because id is a python key word so you need to use _id instead
        self.id = _id
        self.username = username
        self.password = password
