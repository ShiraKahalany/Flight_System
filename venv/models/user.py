class User:
    def __init__(self, id, username, role, first_name, last_name, email, password):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def to_server_format(self):
        return {
            "Id": str(self.id),
            "Username": str(self.username),
            "Role": str(self.role),
            "FirstName": str(self.first_name),
            "LastName": str(self.last_name),
            "Email": str(self.email),
            "Password": str(self.password)
        }

    @classmethod
    def to_client_format(cls, server_dict):
        return cls(
            id=int(server_dict["id"]),
            username=server_dict["username"],
            role=server_dict["role"],
            first_name=server_dict["firstName"],
            last_name=server_dict["lastName"],
            email=server_dict["email"],
            password=server_dict["password"]
        )