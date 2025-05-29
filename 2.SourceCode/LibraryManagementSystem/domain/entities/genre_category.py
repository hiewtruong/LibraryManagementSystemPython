from datetime import datetime

class GenreCategory:
    def __init__(self, genre_category_id=None, name_category=None, genre_category=None, is_deleted=False, created_dt=None, created_by=None, update_dt=None, update_by=None):
        self.genre_category_id = genre_category_id
        self.name_category = name_category
        self.genre_category = genre_category
        self.is_deleted = is_deleted
        self.created_dt = created_dt if created_dt else datetime.now()
        self.created_by = created_by
        self.update_dt = update_dt if update_dt else datetime.now()
        self.update_by = update_by

    def get_genre_category_id(self):
        return self.genre_category_id

    def set_genre_category_id(self, genre_category_id):
        self.genre_category_id = genre_category_id

    def get_name_category(self):
        return self.name_category

    def set_name_category(self, name_category):
        self.name_category = name_category

    def get_genre_category(self):
        return self.genre_category

    def set_genre_category(self, genre_category):
        self.genre_category = genre_category

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