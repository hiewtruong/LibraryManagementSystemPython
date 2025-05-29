class GenreCategoryDTO:
    def __init__(self, genre_category_id=None, name_category=None):
        self.genre_category_id = genre_category_id
        self.name_category = name_category

    def get_genre_category_id(self):
        return self.genre_category_id

    def set_genre_category_id(self, genre_category_id):
        self.genre_category_id = genre_category_id

    def get_name_category(self):
        return self.name_category

    def set_name_category(self, name_category):
        self.name_category = name_category