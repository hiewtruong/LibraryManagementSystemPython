from services.user.i_user_service import IUserService
from views.admin_dashboard_view import Ui_AdminDashboard
from views.author.author_panel import AuthorPanel
from views.user.user_panel import UserPanel

class UserController:
    def __init__(self, user_service: IUserService):
        self.user_service = user_service

    def get_user_by_username(self, root, username, password):
        user_dto = self.user_service.get_user_by_username(username, password, parent=root)
        if user_dto:
            root.hide()
            # Determine which panel to show based on user role or attribute
            role = getattr(user_dto, 'role', '').lower()
            if role == 'author':
                panel = AuthorPanel(controller=self)
            elif role == 'user':
                panel = UserPanel(controller=self)
            else:
                panel = Ui_AdminDashboard(user_dto)
            panel.show()
            return panel
        return None

    def is_email_duplicate(self, email: str) -> bool:
        return self.user_service.is_email_duplicate(email)

    def create_user(self, user_dto) -> bool:
        try:
            return self.user_service.create_user(user_dto)
        except Exception as e:
            print(f"Error creating user: {e}")
            return False

    def get_all_users(self):
        try:
            return self.user_service.get_all_users()
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []

    def update_user(self, user_dto) -> bool:
        try:
            return self.user_service.update_user(user_dto)
        except Exception as e:
            print(f"Error updating user: {e}")
            return False

    def delete_user(self, user_id) -> bool:
        try:
            return self.user_service.delete_user(user_id)
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
