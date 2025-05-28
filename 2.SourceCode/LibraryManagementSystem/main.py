from PyQt5.QtWidgets import QApplication
import sys
from views.login_view import Ui_MainWindow
from controllers.user_controller import UserController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = Ui_MainWindow()
    login_window.show()

    controller = UserController()
    dashboard = None

    def on_login():
        global dashboard
        if dashboard is None:
            result = controller.get_user_by_username(login_window, login_window.username_entry.text(), login_window.password_entry.text())
            if result is not None:
                login_window.hide()
                dashboard = result
                dashboard.show()
                dashboard.raise_()
            else:
                login_window.show()
        else:
            login_window.hide()
            dashboard.show()
            dashboard.raise_()

    try:
        login_window.pushButton.clicked.disconnect()
    except TypeError:
        pass
    login_window.pushButton.clicked.connect(on_login)

    sys.exit(app.exec_())