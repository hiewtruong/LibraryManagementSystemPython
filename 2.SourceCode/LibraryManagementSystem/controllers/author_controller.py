from domain.entities.author import Author
from services.author.author_service import AuthorService
from repositories.author.author_repository import AuthorRepository

class AuthorController:
    def __init__(self, dashboard=None):
        self.author_service = AuthorService(AuthorRepository())
        self.dashboard = dashboard

    def get_all_authors(self):
        return self.author_service.get_all_authors()

    def get_authors_by_name(self, keyword: str):
        return self.author_service.get_authors_by_name(keyword)

    def create_author(self, author: Author) -> bool:
        try:
            return self.author_service.create_author(author)
        except Exception as e:
            print(f"Error creating author: {e}")
            return False

    def update_author(self, author: Author) -> bool:
        try:
            return self.author_service.update_author(author)
        except Exception as e:
            print(f"Error updating author: {e}")
            return False

    def delete_author(self, author_id: int) -> bool:
        try:
            return self.author_service.delete_author(author_id)
        except Exception as e:
            print(f"Error deleting author: {e}")
            return False

    def refresh_author_list(self):
        if self.dashboard and hasattr(self.dashboard, 'current_panel'):
            panel = self.dashboard.current_panel
            if hasattr(panel, 'load_data'):
                panel.load_data()
