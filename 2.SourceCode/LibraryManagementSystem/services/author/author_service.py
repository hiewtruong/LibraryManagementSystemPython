from typing import List
from services.author.i_author_service import IAuthorService
from domain.entities.author import Author
from repositories.author.author_repository import AuthorRepository

class AuthorService(IAuthorService):
    _instance = None

    def __init__(self, author_service: IAuthorService):
        self.author_service = author_service

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls(
                author_service=AuthorRepository()
            )
        return cls._instance

    def get_all_authors(self) -> List[Author]:
        result = self.author_service.get_all_authors()
        return result