from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class CreateTransactionLoanPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: white;")

        self.setMinimumSize(1350, 700)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

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

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Loan Ticket", "User Name", "Email", "Phone", "Total Qty"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)

        # Đặt font cho tiêu đề cột (18px, in đậm)
        header_font = QFont()
        header_font.setPixelSize(18)
        header_font.setBold(True)
        for i in range(self.table.columnCount()):
            header_item = self.table.horizontalHeaderItem(i)
            if header_item:
                header_item.setFont(header_font)

        # Đặt stylesheet chỉ cho màu nền
        self.table.setStyleSheet("""
            alternate-background-color: #f9f9f9;
            background-color: white;
        """)

        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(self.table)
        layout.setStretch(layout.count() - 1, 1)

        self.load_sample_data()

    def load_sample_data(self):
        # Dữ liệu mẫu để hiển thị bảng
        sample_data = [
            {"loan_ticket_number": "LT001", "use_name": "John Doe", "email": "john@example.com", "phone": "1234567890", "total_qty": 3},
            {"loan_ticket_number": "LT002", "use_name": "Jane Smith", "email": "jane@example.com", "phone": "0987654321", "total_qty": 2}
        ]

        self.table.setRowCount(0)
        self.table.setRowCount(len(sample_data))

        # Đặt font cho dữ liệu (15px)
        data_font = QFont()
        data_font.setPixelSize(15)

        for row_idx, data in enumerate(sample_data):
            for col_idx, value in enumerate([data["loan_ticket_number"], data["use_name"], data["email"], data["phone"], str(data["total_qty"])]):
                item = QTableWidgetItem(value)
                item.setFont(data_font)  # Áp dụng font cho từng ô dữ liệu
                self.table.setItem(row_idx, col_idx, item)