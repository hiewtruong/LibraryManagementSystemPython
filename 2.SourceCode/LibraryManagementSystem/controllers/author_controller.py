from domain.entities.author import Author
from services.author.i_author_service import IAuthorService

class AuthorController:
    def __init__(self, author_service: IAuthorService, dashboard=None):
        self.author_service = author_service
        self.dashboard = dashboard

    def get_all_authors(self):
        try:
            print(f"[AuthorController] get_all_authors called. author_service type: {type(self.author_service)}")
            return self.author_service.get_all_authors()
        except Exception as e:
            print(f"Error fetching authors: {e}")
            return []

    def get_authors_by_name(self, keyword: str):
        try:
            return self.author_service.get_authors_by_name(keyword)
        except Exception as e:
            print(f"Error searching authors by name: {e}")
            return []

    def create_author(self, author: Author) -> bool:
        try:
            result = self.author_service.create_author(author)
            return result
        except Exception as e:
            print(f"Error creating author: {e}")
            return False

    def update_author(self, author: Author) -> bool:
        try:
            result = self.author_service.update_author(author)
            return result
        except Exception as e:
            print(f"Error updating author: {e}")
            return False

    def delete_author(self, author_id: int) -> bool:
        try:
            result = self.author_service.delete_author(author_id)
            return result
        except Exception as e:
            print(f"Error deleting author: {e}")
            return False

    def refresh_author_list(self):
        if self.dashboard and hasattr(self.dashboard, 'current_panel'):
            panel = self.dashboard.current_panel
            if hasattr(panel, 'load_author_data'):
                authors = self.get_all_authors()
                panel.load_author_data(authors)

    def confirm_author_deletion(self, author_id):
        # Confirmation handled in author_panel now
        return True
