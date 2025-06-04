from typing import List
from services.category.i_category_service import IGenreCategoryService
from domain.dto.category.category_dto import GenreCategoryDTO
from domain.entities.genre_category import GenreCategory
from repositories.category.category_repository import CategoryRepository
from repositories.category.i_category_repository import ICategoryRepository

class GenreCategoryService(IGenreCategoryService):
    _instance = None

    def __init__(self, category_repository: ICategoryRepository):
        self.genre_category_repository = category_repository

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls(
                category_repository=CategoryRepository()
            )
        return cls._instance

    def get_all_genre_categories(self) -> List[GenreCategoryDTO]:
        result = self.genre_category_repository.get_all_genre_categories()
        dto_list: List[GenreCategoryDTO] = []
        for entity in result:
            dto = GenreCategoryDTO(
                genre_category_id=entity.genre_category_id,
                name_category=entity.name_category
            )
            dto_list.append(dto)

        return dto_list

    def get_in_ids(self, ids: str) -> List[GenreCategoryDTO]:
        result = self.genre_category_repository.get_in_ids(ids)
        dto_list: List[GenreCategoryDTO] = []
        for entity in result:
            dto = GenreCategoryDTO(
                genre_category_id=entity.genre_category_id,
                name_category=entity.name_category
            )
            dto_list.append(dto)

        return dto_list
    
    def find_all(self) -> List[GenreCategory]:
        return self.genre_category_repository.find_all()

    def add_category(self, category: GenreCategory) -> GenreCategory:
        return self.genre_category_repository.add_category(category)
    
    def update_category(self, category: GenreCategory) -> GenreCategory:
        return self.genre_category_repository.update_category(category)
    
    def delete_category(self, genre_category_id: int) -> bool:
        return self.genre_category_repository.delete_category(genre_category_id)