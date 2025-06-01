class UserRoleDTO:
    def __init__(self, user_id=None, first_name=None, last_name=None, user_name=None, password=None, gender=0, email=None, phone=None, address=None, user_role_id_fk=None, is_delete=False, is_admin=False, role_name=None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.password = password
        self.gender = gender
        self.email = email
        self.phone = phone
        self.address = address
        self.user_role_id_fk = user_role_id_fk
        self.is_delete = is_delete
        self.is_admin = is_admin
        self.role_name = role_name

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

    def get_gender(self):
        return self.gender

    def set_gender(self, gender):
        self.gender = gender

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

    def get_user_role_id_fk(self):
        return self.user_role_id_fk

    def set_user_role_id_fk(self, user_role_id_fk):
        self.user_role_id_fk = user_role_id_fk

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

    def from_row(row):
        return UserRoleDTO(
            user_id=row[0],
            first_name=row[1],
            last_name=row[2],
            user_name=row[3],
            password=row[4],
            gender=row[5],
            email=row[6],
            phone=row[7],
            address=row[8],
            user_role_id_fk=row[9],
            is_delete=row[10],
            role_name=row[11],
            is_admin=row[12]
    )