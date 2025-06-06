from abc import ABC, abstractmethod
from typing import List
from domain.entities.author import Author

class IAuthorRepository(ABC):

    @abstractmethod
    def get_all_authors(self) -> List[Author]:
        pass

    @abstractmethod
    def get_authors_by_name(self, keyword: str) -> List[Author]:
        pass

    @abstractmethod
    def create_author(self, author: Author) -> bool:
        pass

    @abstractmethod
    def update_author(self, author: Author) -> bool:
        pass

    @abstractmethod
    def delete_author(self, author_id: int) -> bool:
        """
        Delete author by id. Should check references before deletion.
        """
        pass
