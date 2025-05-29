from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, QSizePolicy
)
from PyQt5.QtCore import Qt
from services.transaction_loan.transaction_loan_service import TransactionLoanService

class TransactionLoanPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: white;")
        self.parent = parent
        self.service = TransactionLoanService.get_instance()

        self.setMinimumSize(1370, 800)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 10, 10)  # Padding cho toàn bộ panel
        main_layout.setSpacing(10)  # Khoảng cách giữa các thành phần

        label = QLabel("Manage Transaction Loan")
        label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            border: none;
            padding-top: 10px;
            background-color: none;
        """)
        label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(label)

        search_layout = QHBoxLayout()
        self.search_column = QComboBox()
        self.search_column.addItems(["LoanTicketNumber", "UserName", "Email", "Phone"])
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter keyword to search...")
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_transactions)

        search_layout.addWidget(self.search_column)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        main_layout.addLayout(search_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Loan Ticket", "User Name", "Email", "Phone", "Total Qty"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            alternate-background-color: #f9f9f9;
            background-color: white;
            border: 0.5px solid;
        """)
        self.table.setContentsMargins(10, 10, 10, 10)  # Padding cho nội dung bảng
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        main_layout.addWidget(self.table)
        main_layout.setStretch(main_layout.count() - 1, 1)

        self.load_data()

    def load_data(self):
        headers = self.service.get_all_transaction_headers("", "")
        self.table.setRowCount(0)
        self.table.setRowCount(len(headers))

        for row_idx, header in enumerate(headers):
            self.table.setItem(row_idx, 0, QTableWidgetItem(header.loan_ticket_number))  # Hiển thị string
            self.table.setItem(row_idx, 1, QTableWidgetItem(header.use_name))
            self.table.setItem(row_idx, 2, QTableWidgetItem(header.email))
            self.table.setItem(row_idx, 3, QTableWidgetItem(header.phone))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(header.total_qty)))

    def search_transactions(self):
        keyword = self.search_input.text().strip()
        column = self.search_column.currentText()

        if not keyword:
            QMessageBox.warning(self, "Warning", "Please enter a keyword to search.")
            return

        headers = self.service.get_all_transaction_headers(keyword, column)
        self.table.setRowCount(0)
        self.table.setRowCount(len(headers))

        for row_idx, header in enumerate(headers):
            self.table.setItem(row_idx, 0, QTableWidgetItem(header.loan_ticket_number))  # Hiển thị string
            self.table.setItem(row_idx, 1, QTableWidgetItem(header.use_name))
            self.table.setItem(row_idx, 2, QTableWidgetItem(header.email))
            self.table.setItem(row_idx, 3, QTableWidgetItem(header.phone))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(header.total_qty)))