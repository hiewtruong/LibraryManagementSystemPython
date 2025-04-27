class Book:
    def __init__(self, book_id, title, author, cover, landing_page, hashtag, genre_category, publisher, publication_date, location, is_display, qty_oh, qty_allocated, is_delete, created_dt, created_by, update_dt, update_by):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.cover = cover
        self.landing_page = landing_page
        self.hashtag = hashtag
        self.genre_category = genre_category
        self.publisher = publisher
        self.publication_date = publication_date
        self.location = location
        self.is_display = is_display
        self.qty_oh = qty_oh
        self.qty_allocated = qty_allocated
        self.is_delete = is_delete
        self.created_dt = created_dt
        self.created_by = created_by
        self.update_dt = update_dt
        self.update_by = update_by