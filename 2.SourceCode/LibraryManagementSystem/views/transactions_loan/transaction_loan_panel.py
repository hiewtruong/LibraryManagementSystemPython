from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class TransactionLoanPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout(self)

        label = QLabel("Quản lý đơn thuê/mượn sách")
        label.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 20px;")
        layout.addWidget(label)
