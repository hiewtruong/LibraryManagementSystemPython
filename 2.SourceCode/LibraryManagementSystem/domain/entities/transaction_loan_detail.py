from datetime import datetime

class TransactionLoanDetail:
    def __init__(self, loan_detail_id=None, loan_book_id=None, is_deleted=False, created_by=None, created_dt=None, update_by=None, update_dt=None, loan_header_id=None):
        self.loan_detail_id = loan_detail_id
        self.loan_book_id = loan_book_id
        self.is_deleted = is_deleted
        self.created_by = created_by
        self.created_dt = created_dt if created_dt else datetime.now()
        self.update_by = update_by
        self.update_dt = update_dt if update_dt else datetime.now()
        self.loan_header_id = loan_header_id

    def get_loan_detail_id(self):
        return self.loan_detail_id

    def set_loan_detail_id(self, loan_detail_id):
        self.loan_detail_id = loan_detail_id

    def get_loan_book_id(self):
        return self.loan_book_id

    def set_loan_book_id(self, loan_book_id):
        self.loan_book_id = loan_book_id

    def get_is_deleted(self):
        return self.is_deleted

    def set_is_deleted(self, is_deleted):
        self.is_deleted = bool(is_deleted)

    def get_created_by(self):
        return self.created_by

    def set_created_by(self, created_by):
        self.created_by = created_by

    def get_created_dt(self):
        return self.created_dt

    def set_created_dt(self, created_dt):
        self.created_dt = created_dt

    def get_update_by(self):
        return self.update_by

    def set_update_by(self, update_by):
        self.update_by = update_by

    def get_update_dt(self):
        return self.update_dt

    def set_update_dt(self, update_dt):
        self.update_dt = update_dt

    def get_loan_header_id(self):
        return self.loan_header_id

    def set_loan_header_id(self, loan_header_id):
        self.loan_header_id = loan_header_id