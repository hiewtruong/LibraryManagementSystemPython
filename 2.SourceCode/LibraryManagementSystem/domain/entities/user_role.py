class UserRole:
    def __init__(self, user_role_id, role_name, is_admin, type, is_delete, created_dt, created_by, update_dt, update_by):
        self.user_role_id = user_role_id
        self.role_name = role_name
        self.is_admin = is_admin
        self.type = type
        self.is_delete = is_delete
        self.created_dt = created_dt
        self.created_by = created_by
        self.update_dt = update_dt
        self.update_by = update_by