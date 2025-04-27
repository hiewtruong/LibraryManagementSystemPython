class User:
    def __init__(self, user_id, first_name, last_name, user_name, password, gender, email, phone, address, user_role_id, is_delete, created_dt, created_by, update_dt, update_by):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.password = password
        self.gender = gender
        self.email = email
        self.phone = phone
        self.address = address
        self.user_role_id = user_role_id
        self.is_delete = is_delete
        self.created_dt = created_dt
        self.created_by = created_by
        self.update_dt = update_dt
        self.update_by = update_by