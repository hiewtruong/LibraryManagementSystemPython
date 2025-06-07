from typing import List
from services.author.i_author_service import IAuthorService
from domain.entities.author import Author
from repositories.author.author_repository import AuthorRepository
from repositories.user.user_repository import UserRepository

class AuthorService(IAuthorService):
    _instance = None

    def __init__(self, author_service: IAuthorService):
        self.author_service = author_service
        self.user_repository = UserRepository()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls(
                author_service=AuthorRepository()
            )
        return cls._instance
    def get_author_by_id(self, author_id):
        # Implement logic to retrieve an author by ID
        authors = self.get_all_authors()
        for author in authors:
            if author.author_id == author_id:
                return author
        return None
    def get_all_authors(self) -> List[Author]:
        authors = self.author_service.get_all_authors()
        self._map_usernames_to_emails(authors)
        return authors

    def get_authors_by_name(self, keyword: str) -> List[Author]:
        authors = self.author_service.get_authors_by_name(keyword)
        self._map_usernames_to_emails(authors)
        return authors

    def create_author(self, author: Author) -> bool:
        return self.author_service.create_author(author)

    def update_author(self, author: Author) -> bool:
        return self.author_service.update_author(author)

    def delete_author(self, author_id: int) -> bool:
        return self.author_service.delete_author(author_id)

    def _map_usernames_to_emails(self, authors: List[Author]):
        for author in authors:
            created_by_username = author.created_by
            update_by_username = author.update_by

            created_by_email = self._get_email_by_username(created_by_username)
            update_by_email = self._get_email_by_username(update_by_username)

            author.created_by = created_by_email if created_by_email else created_by_username
            author.update_by = update_by_email if update_by_email else update_by_username

    def _get_email_by_username(self, username: str) -> str:
        if not username:
            return None
        user = self.user_repository.get_user_by_username(username)
        if user:
            return getattr(user, 'email', None) or getattr(user, 'user_email', None)
        return None
