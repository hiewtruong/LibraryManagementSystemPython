from services.user_service import UserService
from views.admin_dashboard_view import Ui_AdminDashboard
from PyQt5 import QtWidgets

class UserController:
    def __init__(self):
        self.user_service = UserService()

    def get_user_by_username(self, root, username, password):
        userDTO = self.user_service.get_user_by_username(username, password,parent=root)
        if userDTO is not None:
            root.hide()
            dashboard = Ui_AdminDashboard(userDTO)
            return dashboard
        else:
            return None