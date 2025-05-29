from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class CreateTransactionLoanPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout(self)

        label = QLabel("Create Transaction Loan")
        label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            padding: 10px;
            border: none;
            background-color: none;
        """)
        label.setAlignment(Qt.AlignCenter)

        layout.addWidget(label)
