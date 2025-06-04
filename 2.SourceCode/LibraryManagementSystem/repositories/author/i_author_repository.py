from abc import ABC, abstractmethod
from typing import List
from domain.entities.author import Author

class IAuthorRepository(ABC):
    @abstractmethod
    def get_all_authors(self) -> List[Author]:
        pass