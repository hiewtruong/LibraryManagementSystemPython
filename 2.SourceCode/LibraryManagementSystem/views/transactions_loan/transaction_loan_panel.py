from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from lib.constants import TRANS_PAID
from services.transaction_loan.transaction_loan_service import TransactionLoanService
from domain.dto.transaction.transaction_loan_header_request_dto import TransactionLoanHeaderRequestDTO

class TransactionLoanPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: white;")
        self.parent = parent
        self.service = TransactionLoanService.get_instance()
        self.controller = None
        self.headers = []

        self.setMinimumSize(1370, 830)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 10, 10)
        main_layout.setSpacing(10)

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
        search_layout.setAlignment(Qt.AlignLeft)

        search_label = QLabel("Search")
        search_label_font = QFont()
        search_label_font.setPixelSize(13)
        search_label.setFont(search_label_font)
        search_label.setStyleSheet("border: none;")
        search_label.setMaximumWidth(50)

        self.search_column = QComboBox()
        self.search_column.addItems(["LoanTicketNumber", "UserName", "Email", "Phone"])
        self.search_column.setMaximumWidth(180)
        self.search_column.setMinimumHeight(25)
        combo_font = QFont()
        combo_font.setPixelSize(13)
        self.search_column.setFont(combo_font)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter keyword to search...")
        self.search_input.setMaximumWidth(250)
        self.search_input.setMinimumHeight(25)

        self.search_button = QPushButton("Search")
        self.search_button.setFixedWidth(70)
        self.search_button.setFixedHeight(25)
        self.search_button.setStyleSheet("""
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
        """)
        self.search_button.clicked.connect(self.search_transactions)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_column)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        search_layout.setSpacing(8)
        main_layout.addLayout(search_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Loan Ticket", "User Name", "Email", "Phone", "Total Qty", "Status", "Return Loan Date"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            alternate-background-color: #f9f9f9;
            background-color: white;
            border: 0.5px solid;
        """)
        self.table.setContentsMargins(10, 10, 10, 10)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        header_font = QFont()
        header_font.setPixelSize(13)
        header_font.setBold(True)
        for i in range(self.table.columnCount()):
            header_item = self.table.horizontalHeaderItem(i)
            if header_item:
                header_item.setFont(header_font)

        main_layout.addWidget(self.table)
        main_layout.setStretch(main_layout.count() - 1, 1)

        self.table.doubleClicked.connect(self.show_detail_dialog)

    def load_data(self):
        if self.controller:
            self.controller.load_transaction_headers(self)

    def update_table(self, headers):
        self.headers = headers
        self.table.setRowCount(0)
        self.table.setRowCount(len(self.headers))
        data_font = QFont()
        data_font.setPixelSize(12)

        for row_idx, header in enumerate(self.headers):
            return_loan_date = header.get_loan_return_dt().date() if header.get_loan_return_dt() else None
            return_loan_date_str = return_loan_date.strftime("%m-%d-%Y") if return_loan_date else "N/A"

            items = [
                QTableWidgetItem(header.loan_ticket_number),
                QTableWidgetItem(header.use_name),
                QTableWidgetItem(header.email),
                QTableWidgetItem(header.phone),
                QTableWidgetItem(str(header.total_qty)),
                QTableWidgetItem(header.status_name),
                QTableWidgetItem(return_loan_date_str)
            ]
            if header.expired == 1:
                for item in items:
                    item.setForeground(QColor("red"))
            if getattr(header, 'status', None) == TRANS_PAID:
                for item in items:
                    item.setForeground(QColor("green"))
            for col_idx, item in enumerate(items):
                item.setFont(data_font)
                if col_idx == 4:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                elif col_idx == 5:
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                self.table.setItem(row_idx, col_idx, item)

    def search_transactions(self):
        keyword = self.search_input.text().strip()
        column = self.search_column.currentText()

        if not keyword:
            QMessageBox.warning(self, "Warning", "Please enter a keyword to search.")
            return

        if self.controller:
            self.controller.search_transaction_headers(self, keyword, column)

    def update_search_table(self, headers):
        self.headers = headers
        self.table.setRowCount(0)
        self.table.setRowCount(len(self.headers))
        data_font = QFont()
        data_font.setPixelSize(12)

        for row_idx, header in enumerate(self.headers):
            return_loan_date = header.get_loan_return_dt().date() if header.get_loan_return_dt() else None
            return_loan_date_str = return_loan_date.strftime("%m-%d-%Y") if return_loan_date else "N/A"

            items = [
                QTableWidgetItem(header.loan_ticket_number),
                QTableWidgetItem(header.use_name),
                QTableWidgetItem(header.email),
                QTableWidgetItem(header.phone),
                QTableWidgetItem(str(header.total_qty)),
                QTableWidgetItem(header.status_name),
                QTableWidgetItem(return_loan_date_str)
            ]
            if header.expired == 1:
                for item in items:
                    item.setForeground(QColor("red"))
            if getattr(header, 'status', None) == TRANS_PAID:
                for item in items:
                    item.setForeground(QColor("green"))
            for col_idx, item in enumerate(items):
                item.setFont(data_font)
                if col_idx == 4:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                elif col_idx == 5:
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                self.table.setItem(row_idx, col_idx, item)

    def show_detail_dialog(self, item):
        row = self.table.currentRow()
        if row >= 0 and row < len(self.headers):
            header_dto = self.headers[row]
            if self.controller:
                self.controller.view_transaction_detail(self, self, header_dto)