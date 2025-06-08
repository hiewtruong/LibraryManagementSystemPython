from services.user.i_user_service import IUserService
# from views.admin_dashboard_view import Ui_AdminDashboard
from views.author.author_panel import AuthorPanel
from views.user.user_panel import UserPanel
from services.author.author_service import AuthorService
from repositories.author.author_repository import AuthorRepository
from controllers.author_controller import AuthorController

class UserController:
    def __init__(self, user_service: IUserService):
        self.user_service = user_service

    def get_user_by_username(self, root, username, password):
        user_dto = self.user_service.get_user_by_username(username, password, parent=root)
        if user_dto:
            root.hide()
            role = getattr(user_dto, 'role', '').lower()
            panel = None
            from views.admin_dashboard_view import Ui_AdminDashboard
            panel = Ui_AdminDashboard(user_dto)
            panel.show()
            return panel

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

    def notify_user_added(self):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self.dashboard, "Success", "User added successfully.")
        self.refresh_user_list()

    def notify_user_updated(self):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self.dashboard, "Success", "User updated successfully.")
        self.refresh_user_list()

    def notify_user_deleted(self):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self.dashboard, "Success", "User deleted successfully.")
        self.refresh_user_list()

    def notify_controller_missing(self):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.warning(self.dashboard, "Warning", "Controller not set.")

    def confirm_user_deletion(self, user_id):
        from PyQt5.QtWidgets import QMessageBox
        reply = QMessageBox.question(
            self.dashboard,
            "Confirm Delete",
            "Do you want to delete?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        return reply == QMessageBox.Yes

    def refresh_user_list(self):
        if self.dashboard and hasattr(self.dashboard, 'current_panel'):
            panel = self.dashboard.current_panel
            if hasattr(panel, 'load_user_data'):
                users = self.get_all_users()
                panel.load_user_data(users)