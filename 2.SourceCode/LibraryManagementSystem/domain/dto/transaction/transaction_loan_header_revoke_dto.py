from domain.dto.transaction.transaction_loan_detail_request_dto import TransactionLoanDetailRequestDTO


class TransactionLoanHeaderRevokeDTO:
    def __init__(self, loan_header_id=None, loan_details:TransactionLoanDetailRequestDTO=[]):
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