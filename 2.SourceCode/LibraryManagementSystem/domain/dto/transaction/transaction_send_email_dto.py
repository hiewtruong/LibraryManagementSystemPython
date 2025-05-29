from datetime import datetime

class TransactionSendEmailDTO:
    def __init__(self, loan_ticket_number=None, use_name=None, email=None, phone=None, total_qty=0, loan_dt=None, loan_return_dt=None, book_details=None):
        self.loan_ticket_number = loan_ticket_number
        self.use_name = use_name
        self.email = email
        self.phone = phone
        self.total_qty = total_qty
        self.loan_dt = loan_dt
        self.loan_return_dt = loan_return_dt
        self.book_details = book_details if book_details is not None else []

    def get_loan_ticket_number(self):
        return self.loan_ticket_number

    def set_loan_ticket_number(self, loan_ticket_number):
        self.loan_ticket_number = loan_ticket_number

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

    def get_book_details(self):
        return self.book_details

    def set_book_details(self, book_details):
        self.book_details = book_details