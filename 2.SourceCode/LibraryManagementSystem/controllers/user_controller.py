from services.user.i_user_service import IUserService
from views.admin_dashboard_view import Ui_AdminDashboard

class UserController:
    def __init__(self, user_service: IUserService):
        self.user_service = user_service

    def get_user_by_username(self, root, username, password):
        user_dto = self.user_service.get_user_by_username(username, password, parent=root)
        if user_dto:
            root.hide()
            dashboard = Ui_AdminDashboard(user_dto)
            dashboard.show()
            return dashboard
        return None
