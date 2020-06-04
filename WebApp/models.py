# A user class for storing information during token creation
class User:
    def __init__(self, username, first_name, last_name, admin):
        self.username = username
        self.admin = admin
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f"User('{self.username}', '{self.first_name}', '{self.last_name}', '{self.admin}')"
