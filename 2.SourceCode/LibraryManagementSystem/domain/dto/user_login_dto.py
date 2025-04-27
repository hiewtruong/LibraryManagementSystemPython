class UserLoginDTO:
    def __init__(self, user_name, password, user_role_id, role_name):
        self.user_name = user_name
        self.password = password
        self.user_role_id = user_role_id
        self.role_name = role_name