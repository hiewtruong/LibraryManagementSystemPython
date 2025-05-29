class TransactionLoanDetailRequestDTO:
    def __init__(self, load_book_id=None):
        self.load_book_id = load_book_id

    def get_load_book_id(self):
        return self.load_book_id

    def set_load_book_id(self, load_book_id):
        self.load_book_id = load_book_id