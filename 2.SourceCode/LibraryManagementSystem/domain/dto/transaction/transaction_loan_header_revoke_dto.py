class TransactionLoanHeaderRevokeDTO:
    def __init__(self, loan_header_id=None, loan_details=None):
        self.loan_header_id = loan_header_id
        self.loan_details = loan_details if loan_details is not None else []

    def get_loan_header_id(self):
        return self.loan_header_id

    def set_loan_header_id(self, loan_header_id):
        self.loan_header_id = loan_header_id

    def get_loan_details(self):
        return self.loan_details

    def set_loan_details(self, loan_details):
        self.loan_details = loan_details