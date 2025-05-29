class BookSendEmail:
    def __init__(self, book_id=None, title=None, author=None):
        self.book_id = book_id
        self.title = title
        self.author = author

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