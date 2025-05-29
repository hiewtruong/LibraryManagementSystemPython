from datetime import datetime

class TransactionLoanDetailDTO:
    def __init__(self, loan_detail_id=None, loan_header_id=None, loan_book_id=None, created_by=None, created_dt=None, update_by=None, update_dt=None, book_id=None, title=None, author=None, genre_category=None, publisher=None, publish_year=None):
        self.loan_detail_id = loan_detail_id
        self.loan_header_id = loan_header_id
        self.loan_book_id = loan_book_id
        self.created_by = created_by
        self.created_dt = created_dt if created_dt else datetime.now()
        self.update_by = update_by
        self.update_dt = update_dt if update_dt else datetime.now()
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre_category = genre_category
        self.publisher = publisher
        self.publish_year = publish_year

    def get_loan_detail_id(self):
        return self.loan_detail_id

    def set_loan_detail_id(self, loan_detail_id):
        self.loan_detail_id = loan_detail_id

    def get_loan_header_id(self):
        return self.loan_header_id

    def set_loan_header_id(self, loan_header_id):
        self.loan_header_id = loan_header_id

    def get_loan_book_id(self):
        return self.loan_book_id

    def set_loan_book_id(self, loan_book_id):
        self.loan_book_id = loan_book_id

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

    def get_book_id(self):
        return self.book_id

    def set_book_id(self, book_id):
        self.book_id = book_id

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def get_author(self):
        return self.author

    def set_author(self, author):
        self.author = author

    def get_genre_category(self):
        return self.genre_category

    def set_genre_category(self, genre_category):
        self.genre_category = genre_category

    def get_publisher(self):
        return self.publisher

    def set_publisher(self, publisher):
        self.publisher = publisher

    def get_publish_year(self):
        return self.publish_year

    def set_publish_year(self, publish_year):
        self.publish_year = publish_year