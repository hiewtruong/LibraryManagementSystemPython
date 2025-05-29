from PyQt5.QtWidgets import QApplication
import sys
from views.login_view import Ui_MainWindow
from controllers.user_controller import UserController
from services.user.user_service import UserService
from repositories.user.user_repository import UserRepository

if __name__ == "__main__":
    app = QApplication(sys.argv)
    user_service = UserService(UserRepository())
    controller = UserController(user_service)
    login_window = Ui_MainWindow(controller)
    login_window.show()
    sys.exit(app.exec_())