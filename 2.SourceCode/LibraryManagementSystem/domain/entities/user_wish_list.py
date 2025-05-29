from datetime import datetime

class UserWishList:
    def __init__(self, user_wish_list_id=None, user_id=None, book_id=None, is_deleted=False, created_dt=None, created_by=None, update_dt=None, update_by=None):
        self.user_wish_list_id = user_wish_list_id
        self.user_id = user_id
        self.book_id = book_id
        self.is_deleted = is_deleted
        self.created_dt = created_dt if created_dt else datetime.now()
        self.created_by = created_by
        self.update_dt = update_dt if update_dt else datetime.now()
        self.update_by = update_by

    def get_user_wish_list_id(self):
        return self.user_wish_list_id

    def set_user_wish_list_id(self, user_wish_list_id):
        self.user_wish_list_id = user_wish_list_id

    def get_user_id(self):
        return self.user_id

    def set_user_id(self, user_id):
        self.user_id = user_id

    def get_book_id(self):
        return self.book_id

    def set_book_id(self, book_id):
        self.book_id = book_id

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