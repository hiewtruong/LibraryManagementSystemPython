from datetime import datetime

class BookDTO:
    def __init__(self, book_id=None, title=None, author=None, cover=None, landing_page=None, hashtag=None, genre_category=None, publisher=None, publish_year=None, location=None, is_display=0, qty_oh=0, qty_allocated=0, is_delete=0, created_dt=None, created_by=None, update_dt=None, update_by=None):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.cover = cover
        self.landing_page = landing_page
        self.hashtag = hashtag
        self.genre_category = genre_category
        self.publisher = publisher
        self.publish_year = publish_year
        self.location = location
        self.is_display = is_display
        self.qty_oh = qty_oh
        self.qty_allocated = qty_allocated
        self.is_delete = is_delete
        self.created_dt = created_dt if created_dt else datetime.now()
        self.created_by = created_by
        self.update_dt = update_dt if update_dt else datetime.now()
        self.update_by = update_by

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

    def get_cover(self):
        return self.cover

    def set_cover(self, cover):
        self.cover = cover

    def get_landing_page(self):
        return self.landing_page

    def set_landing_page(self, landing_page):
        self.landing_page = landing_page

    def get_hashtag(self):
        return self.hashtag

    def set_hashtag(self, hashtag):
        self.hashtag = hashtag

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

    def get_location(self):
        return self.location

    def set_location(self, location):
        self.location = location

    def get_is_display(self):
        return self.is_display

    def set_is_display(self, is_display):
        self.is_display = is_display

    def get_qty_oh(self):
        return self.qty_oh

    def set_qty_oh(self, qty_oh):
        self.qty_oh = qty_oh

    def get_qty_allocated(self):
        return self.qty_allocated

    def set_qty_allocated(self, qty_allocated):
        self.qty_allocated = qty_allocated

    def get_is_delete(self):
        return self.is_delete

    def set_is_delete(self, is_delete):
        self.is_delete = is_delete

    def get_created_dt(self):
        return self.created_dt

    def set_created_dt(self, created_dt):
        self.created_dt = created_dt

    def get_created_by(self):
        return self.created_by

    def set_created_by(self, created_by):
        self.created_by = created_by

    def get_update_dt(self):
        return self.update_dt

    def set_update_dt(self, update_dt):
        self.update_dt = update_dt

    def get_update_by(self):
        return self.update_by

    def set_update_by(self, update_by):
        self.update_by = update_by