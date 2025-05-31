from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt

class ConfirmModal(QDialog):
    def __init__(self, parent=None, message="Are you sure?", title="Confirmation"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(300, 130)

        self.result = None

        self._init_ui(message)

    def _init_ui(self, message):
        layout = QVBoxLayout()

        self.label = QLabel(message)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignLeft)
        self.label.setStyleSheet("font-size: 14px; padding: 10px; border: none")
        layout.addWidget(self.label)

        button_layout = QHBoxLayout()

        self.yes_button = QPushButton("Yes")
        self.yes_button.setStyleSheet("background-color: #28a745; color: white; font-weight: bold;")
        self.yes_button.clicked.connect(self._on_yes)
        button_layout.addWidget(self.yes_button)

        self.no_button = QPushButton("No")
        self.no_button.setStyleSheet("background-color: #dc3545; color: white; font-weight: bold;")
        self.no_button.clicked.connect(self._on_no)
        button_layout.addWidget(self.no_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def _on_yes(self):
        self.accept()

    def _on_no(self):
        self.reject()
