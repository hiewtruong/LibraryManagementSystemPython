from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class NotificationModal(QDialog):
    def __init__(self, parent=None, message="", title="Notification", color="#007bff", icon_path=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(350, 150)

        if icon_path:
            self.setWindowIcon(QIcon(icon_path))

        layout = QVBoxLayout()

        self.label = QLabel(message)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 14px; padding: 10px;")
        layout.addWidget(self.label)

        close_button = QPushButton("OK")
        close_button.setStyleSheet(f"background-color: {color}; color: white; font-weight: bold;")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)


class ErrorModal(NotificationModal):
    def __init__(self, parent=None, message="An error has occurred"):
        super().__init__(parent, message, "Error", color="#dc3545")  # Red


class SuccessModal(NotificationModal):
    def __init__(self, parent=None, message="Operation successful"):
        super().__init__(parent, message, "Success", color="#28a745")  # Green


class WarningModal(NotificationModal):
    def __init__(self, parent=None, message="This is a warning"):
        super().__init__(parent, message, "Warning", color="#ffc107")  # Yellow
