from datetime import datetime

class Author:
    def __init__(self, author_id=None, author_name=None, is_deleted=False, created_dt=None, created_by=None, update_dt=None, update_by=None):
        self.author_id = author_id
        self.author_name = author_name
        self.is_deleted = is_deleted
        self.created_dt = created_dt if created_dt else datetime.now() 
        self.created_by = created_by
        self.update_dt = update_dt if update_dt else datetime.now()
        self.update_by = update_by

    @classmethod
    def from_basic_info(cls, author_name, created_by, update_by):
        return cls(author_name=author_name, created_by=created_by, update_by=update_by)

    def get_author_id(self):
        return self.author_id

    def set_author_id(self, author_id):
        self.author_id = author_id

    def get_author_name(self):
        return self.author_name

    def set_author_name(self, author_name):
        self.author_name = author_name

    def get_is_deleted(self):
        return self.is_deleted

    def set_is_deleted(self, is_deleted):
        self.is_deleted = bool(is_deleted)

    def get_created_dt(self):
        return self.created_dt

    def set_created_dt(self, created_dt):
        self.created_dt = created_dt if created_dt else datetime.now()

    def get_created_by(self):
        return self.created_by

    def set_created_by(self, created_by):
        self.created_by = created_by

    def get_update_dt(self):
        return self.update_dt

    def set_update_dt(self, update_dt):
        self.update_dt = update_dt if update_dt else datetime.now()

    def get_update_by(self):
        return self.update_by

    def set_update_by(self, update_by):
        self.update_by = update_by