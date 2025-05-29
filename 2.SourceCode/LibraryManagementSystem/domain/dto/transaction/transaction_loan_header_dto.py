from datetime import datetime

class TransactionLoanHeaderDTO:
    def __init__(self, loan_header_id=None, loan_ticket_number=None, user_id=None, use_name=None, email=None, phone=None, total_qty=0, loan_dt=None, loan_return_dt=None, created_by=None, created_dt=None, update_by=None, update_dt=None, status=0, status_name=None):
        self.loan_header_id = loan_header_id
        self.loan_ticket_number = loan_ticket_number
        self.user_id = user_id
        self.use_name = use_name
        self.email = email
        self.phone = phone
        self.total_qty = total_qty
        self.loan_dt = loan_dt
        self.loan_return_dt = loan_return_dt
        self.created_by = created_by
        self.created_dt = created_dt if created_dt else datetime.now()
        self.update_by = update_by
        self.update_dt = update_dt if update_dt else datetime.now()
        self.status = status
        self.status_name = status_name

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

    def get_use_name(self):
        return self.use_name

    def set_use_name(self, use_name):
        self.use_name = use_name

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_phone(self):
        return self.phone

    def set_phone(self, phone):
        self.phone = phone

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

    def get_status_name(self):
        return self.status_name

    def set_status_name(self, status_name):
        self.status_name = status_name

    def from_row(row):
        return TransactionLoanHeaderDTO(
        loan_header_id=row[0],
        loan_ticket_number=row[1],
        user_id=row[2],
        use_name=row[3],
        email=row[4],
        phone=row[5],
        total_qty=row[6],
        loan_dt=row[7],
        loan_return_dt=row[8],
        created_by=row[9],
        created_dt=row[10],
        update_by=row[11],
        update_dt=row[12],
        status=row[13]
    )