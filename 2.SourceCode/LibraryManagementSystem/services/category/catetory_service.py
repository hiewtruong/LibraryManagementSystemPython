from typing import List
from services.category.i_category_service import IGenreCategoryService
from domain.dto.category.category_dto import GenreCategoryDTO
from repositories.category.category_repository import CategoryRepository
from repositories.category.i_category_repository import ICategoryRepository

class GenreCategoryService(IGenreCategoryService):
    _instance = None

    def __init__(self):
        self.genre_category_repository: ICategoryRepository = CategoryRepository.get_instance()

    @staticmethod
    def get_instance():
        if GenreCategoryService._instance is None:
            GenreCategoryService._instance = GenreCategoryService()
        return GenreCategoryService._instance

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
