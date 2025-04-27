class TransactionLoanDetail:
    def __init__(self, loan_detail_id, load_book_id, is_delete, created_dt, created_by, update_dt, update_by):
        self.loan_detail_id = loan_detail_id
        self.load_book_id = load_book_id
        self.is_delete = is_delete
        self.created_dt = created_dt
        self.created_by = created_by
        self.update_dt = update_dt
        self.update_by = update_by