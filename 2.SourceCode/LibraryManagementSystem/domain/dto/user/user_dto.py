class UserDTO:
    def __init__(self, user_id=None, first_name=None, last_name=None, user_name=None, password=None, email=None, phone=None, address=None, gender=None, user_role_id=None, is_delete=False, is_admin=False, role_name=None, created_dt=None, created_by=None, update_dt=None, update_by=None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.password = password
        self.email = email
        self.phone = phone
        self.address = address
        self.gender = gender
        self.user_role_id = user_role_id
        self.is_delete = is_delete
        self.is_admin = is_admin
        self.role_name = role_name
        self.created_dt = created_dt
        self.created_by = created_by
        self.update_dt = update_dt
        self.update_by = update_by

    def get_user_id(self):
        return self.user_id

    def set_user_id(self, user_id):
        self.user_id = user_id

    def get_first_name(self):
        return self.first_name

    def set_first_name(self, first_name):
        self.first_name = first_name

    def get_last_name(self):
        return self.last_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def get_user_name(self):
        return self.user_name

    def set_user_name(self, user_name):
        self.user_name = user_name

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_phone(self):
        return self.phone

    def set_phone(self, phone):
        self.phone = phone

    def get_address(self):
        return self.address

    def set_address(self, address):
        self.address = address

    def get_is_delete(self):
        return self.is_delete

    def set_is_delete(self, is_delete):
        self.is_delete = bool(is_delete)

    def get_is_admin(self):
        return self.is_admin

    def set_is_admin(self, is_admin):
        self.is_admin = bool(is_admin)

    def get_role_name(self):
        return self.role_name

    def set_role_name(self, role_name):
        self.role_name = role_name

    def get_gender(self):
        return self.gender

    def set_gender(self, gender):
        self.gender = gender

    def get_user_role_id(self):
        return self.user_role_id

    def set_user_role_id(self, user_role_id):
        self.user_role_id = user_role_id

    def get_created_dt(self):
        return self.created_dt

    def set_created_dt(self, created_dt):
        self.created_dt = created_dt

    def get_created_by(self):
        return self.created_by

    def set_created_by(self, created_by):
        self.created_by = created_by

    def get_update_dt(self):
        return self.update_dt

    def set_update_dt(self, update_dt):
        self.update_dt = update_dt

    def get_update_by(self):
        return self.update_by

    def set_update_by(self, update_by):
        self.update_by = update_by
