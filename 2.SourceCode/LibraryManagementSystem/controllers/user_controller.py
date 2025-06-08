from services.user.i_user_service import IUserService

class UserController:
    def __init__(self, user_service: IUserService):
        self.user_service = user_service

    def get_user_by_username(self, root, username, password):
        from views.admin_dashboard_view import Ui_AdminDashboard
        user_dto = self.user_service.get_user_by_username(username, password, parent=root)
        if user_dto:
            root.hide()
            panel = Ui_AdminDashboard(user_dto)
            panel.show()
            return panel
        else:
            print("Invalid username or password.")
        return None

    def is_email_duplicate(self, email: str) -> bool:
        try:
            return self.user_service.is_email_duplicate(email)
        except Exception as e:
            print(f"Error checking email duplication: {e}")
            return False

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
            print(f"Error fetching users: {e}")
            return []

    def refresh_user_list(self):
        if self.dashboard and hasattr(self.dashboard, 'current_panel'):
            panel = self.dashboard.current_panel
            if hasattr(panel, 'load_user_data'):
                users = self.get_all_users()
                panel.load_user_data(users)
