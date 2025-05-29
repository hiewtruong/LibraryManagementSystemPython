from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image
from lib.constants import MISSING_USER_OR_PASSWORD, ERROR
import os
import io

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, controller):
        self.dashboard = None
        super().__init__()
        self.controller = controller
        self.setupUi(self)
        self._center_window(800, 400)
        self.setFixedSize(800, 400)
        self.pushButton.clicked.connect(self.handle_login)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Library Management - Admin Login")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        main_layout = QtWidgets.QHBoxLayout(self.centralwidget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        left_widget = QtWidgets.QWidget()
        left_widget.setFixedWidth(400)
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setAlignment(QtCore.Qt.AlignCenter)

        image_path = os.path.join("resources", "img", "career-planning.png")
        if os.path.exists(image_path):
            image = Image.open(image_path)
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(buffer.getvalue())
            bg_label = QtWidgets.QLabel()
            bg_label.setPixmap(pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio))
            bg_label.setAlignment(QtCore.Qt.AlignCenter)
            left_layout.addWidget(bg_label)
        else:
            bg_label = QtWidgets.QLabel("Not Found Image")
            bg_label.setStyleSheet("background-color: gray; color: white;")
            bg_label.setAlignment(QtCore.Qt.AlignCenter)
            left_layout.addWidget(bg_label)

        main_layout.addWidget(left_widget)

        right_widget = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right_widget)
        right_layout.setAlignment(QtCore.Qt.AlignCenter)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(10)

        self.label = QtWidgets.QLabel("Admin Login")
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #333;")
        right_layout.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)
        right_layout.addSpacing(15)

        username_layout = QtWidgets.QVBoxLayout()
        self.label_2 = QtWidgets.QLabel("Username:")
        self.label_2.setStyleSheet("color: #333;")
        username_layout.addWidget(self.label_2)

        self.username_entry = QtWidgets.QLineEdit()
        self.username_entry.setFixedWidth(300)
        self.username_entry.setFixedHeight(30)
        self.username_entry.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 5px;
                background-color: white;
            }
        """)
        username_layout.addWidget(self.username_entry)
        right_layout.addLayout(username_layout)
        right_layout.addSpacing(0)

        password_layout = QtWidgets.QVBoxLayout()
        self.label_3 = QtWidgets.QLabel("Password:")
        self.label_3.setStyleSheet("color: #333;")
        password_layout.addWidget(self.label_3)

        self.password_entry = QtWidgets.QLineEdit()
        self.password_entry.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_entry.setFixedWidth(300)
        self.password_entry.setFixedHeight(30)
        self.password_entry.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 5px;
                background-color: white;
            }
        """)
        password_layout.addWidget(self.password_entry)
        right_layout.addLayout(password_layout)
        right_layout.addSpacing(30)

        self.pushButton = QtWidgets.QPushButton("LOGIN")
        self.pushButton.setFixedWidth(300)
        self.pushButton.setFixedHeight(30)
        self.pushButton.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: 2px solid #2ecc71;
                border-radius: 15px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
                border: 2px solid #27ae60;
            }
            QPushButton:pressed {
                background-color: #219653;
                border: 2px solid #219653;
            }
        """)
        right_layout.addWidget(self.pushButton, alignment=QtCore.Qt.AlignCenter)

        main_layout.addWidget(right_widget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Library Management - Admin Login"))
        self.label.setText(_translate("MainWindow", "Admin Login"))
        self.label_2.setText(_translate("MainWindow", "Username:"))
        self.label_3.setText(_translate("MainWindow", "Password:"))
        self.pushButton.setText(_translate("MainWindow", "Login"))

    def _center_window(self, width, height):
        screen = self.screen().availableGeometry()
        screen_width = screen.width()
        screen_height = screen.height()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.setGeometry(x, y, width, height)

    def handle_login(self):
        username = self.username_entry.text().strip()
        password = self.password_entry.text().strip()

        if not username or not password:
            QtWidgets.QMessageBox.warning(self, ERROR, MISSING_USER_OR_PASSWORD)
            return
        try:
            result = self.controller.get_user_by_username(self, username, password)
            if result is not None:
                self.dashboard = result
                self.hide()
                self.dashboard.show()
                self.dashboard.raise_()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error System", f"Can't login: {str(e)}")
