from datetime import datetime

class UserRole:
    def __init__(self, user_role_id=None, role_name=None, is_admin=False, type=None, is_deleted=False, created_dt=None, created_by=None, update_dt=None, update_by=None):
        self.user_role_id = user_role_id
        self.role_name = role_name
        self.is_admin = is_admin
        self.type = type
        self.is_deleted = is_deleted
        self.created_dt = created_dt if created_dt else datetime.now()
        self.created_by = created_by
        self.update_dt = update_dt if update_dt else datetime.now()
        self.update_by = update_by

    def get_user_role_id(self):
        return self.user_role_id

    def set_user_role_id(self, user_role_id):
        self.user_role_id = user_role_id

    def get_role_name(self):
        return self.role_name

    def set_role_name(self, role_name):
        self.role_name = role_name

    def get_is_admin(self):
        return self.is_admin

    def set_is_admin(self, is_admin):
        self.is_admin = bool(is_admin)

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

    def get_is_deleted(self):
        return self.is_deleted

    def set_is_deleted(self, is_deleted):
        self.is_deleted = bool(is_deleted)

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