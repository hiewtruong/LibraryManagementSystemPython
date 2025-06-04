from abc import ABC, abstractmethod
from typing import List
from domain.entities.genre_category import GenreCategory

class ICategoryRepository(ABC):
    @abstractmethod
    def get_all_genre_categories(self) -> List[GenreCategory]:
        pass
    @abstractmethod
    def get_in_ids(self, ids: str) -> List[GenreCategory]:
        pass
    @abstractmethod
    def find_all(self) -> List[GenreCategory]:
        pass
    @abstractmethod
    def add_category(self, category: GenreCategory) -> GenreCategory:
        pass
    @abstractmethod
    def update_category(self, category: GenreCategory) -> GenreCategory:
        pass
    @abstractmethod
    def delete_category(self, genre_category_id: int) -> bool:
        pass
    @abstractmethod
    def get_category_by_id(self, genre_category_id: int) -> GenreCategory:
        pass