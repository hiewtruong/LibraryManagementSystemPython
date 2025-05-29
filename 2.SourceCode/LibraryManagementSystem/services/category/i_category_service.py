from typing import List
from domain.dto.category.category_dto import GenreCategoryDTO

class IGenreCategoryService:
    def get_all_genre_categories(self) -> List[GenreCategoryDTO]:
        raise NotImplementedError
