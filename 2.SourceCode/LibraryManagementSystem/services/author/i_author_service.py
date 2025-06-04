from typing import List
from domain.entities.author import Author
from abc import ABC, abstractmethod

class IAuthorService(ABC):
    @abstractmethod
    def get_all_authors(self) -> List[Author]:
        pass
