from abc import ABC, abstractmethod
from typing import List
from domain.entities.genre_category import GenreCategory

class ICategoryRepository(ABC):
    @abstractmethod
    def get_all_genre_categories(self) -> List[GenreCategory]:
        pass
