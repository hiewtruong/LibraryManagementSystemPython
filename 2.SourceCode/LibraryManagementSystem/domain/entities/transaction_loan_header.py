from datetime import datetime

class TransactionLoanHeader:
    def __init__(self, loan_header_id=None, loan_ticket_number=None, user_id=None, total_qty=0, loan_dt=None, loan_return_dt=None, is_deleted=False, created_by=None, created_dt=None, update_by=None, update_dt=None, status=0):
        self.loan_header_id = loan_header_id
        self.loan_ticket_number = loan_ticket_number
        self.user_id = user_id
        self.total_qty = total_qty
        self.loan_dt = loan_dt
        self.loan_return_dt = loan_return_dt
        self.is_deleted = is_deleted
        self.created_by = created_by
        self.created_dt = created_dt if created_dt else datetime.now()
        self.update_by = update_by
        self.update_dt = update_dt if update_dt else datetime.now()
        self.status = status

    def get_loan_header_id(self):
        return self.loan_header_id

    def set_loan_header_id(self, loan_header_id):
        self.loan_header_id = loan_header_id

    def get_loan_ticket_number(self):
        return self.loan_ticket_number

    def set_loan_ticket_number(self, loan_ticket_number):
        self.loan_ticket_number = loan_ticket_number

    def get_user_id(self):
        return self.user_id

    def set_user_id(self, user_id):
        self.user_id = user_id

    def get_total_qty(self):
        return self.total_qty

    def set_total_qty(self, total_qty):
        self.total_qty = total_qty

    def get_loan_dt(self):
        return self.loan_dt

    def set_loan_dt(self, loan_dt):
        self.loan_dt = loan_dt

    def get_loan_return_dt(self):
        return self.loan_return_dt

    def set_loan_return_dt(self, loan_return_dt):
        self.loan_return_dt = loan_return_dt

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

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status