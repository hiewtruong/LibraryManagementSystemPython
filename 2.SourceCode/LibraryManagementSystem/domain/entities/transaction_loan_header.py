class TransactionLoanHeader:
    def __init__(self, loan_header_id, loan_ticket_number, user_id, total_qty, loan_dt, loan_return_dt, is_delete, created_dt, created_by, update_dt, update_by):
        self.loan_header_id = loan_header_id
        self.loan_ticket_number = loan_ticket_number
        self.user_id = user_id
        self.total_qty = total_qty
        self.loan_dt = loan_dt
        self.loan_return_dt = loan_return_dt
        self.is_delete = is_delete
        self.created_dt = created_dt
        self.created_by = created_by
        self.update_dt = update_dt
        self.update_by = update_by