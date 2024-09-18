class User:
    def __init__(self, id, username, role, first_name, last_name, email, password):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
