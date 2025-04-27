class UserWishList:
    def __init__(self, user_wish_list_id, user_id, book_id, is_delete, created_dt, created_by, update_dt, update_by):
        self.user_wish_list_id = user_wish_list_id
        self.user_id = user_id
        self.book_id = book_id
        self.is_delete = is_delete
        self.created_dt = created_dt
        self.created_by = created_by
        self.update_dt = update_dt
        self.update_by = update_by