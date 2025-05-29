from datetime import datetime

class TransactionLoanHeaderRequestDTO:
    def __init__(self, user_id=None, total_qty=0, loan_return_dt=None, loan_details=None):
        self.user_id = user_id
        self.total_qty = total_qty
        self.loan_return_dt = loan_return_dt
        self.loan_details = loan_details if loan_details is not None else []

    def get_user_id(self):
        return self.user_id

    def set_user_id(self, user_id):
        self.user_id = user_id

    def get_total_qty(self):
        return self.total_qty

    def set_total_qty(self, total_qty):
        self.total_qty = total_qty

    def get_loan_return_dt(self):
        return self.loan_return_dt

    def set_loan_return_dt(self, loan_return_dt):
        self.loan_return_dt = loan_return_dt

    def get_loan_details(self):
        return self.loan_details

    def set_loan_details(self, loan_details):
        self.loan_details = loan_details