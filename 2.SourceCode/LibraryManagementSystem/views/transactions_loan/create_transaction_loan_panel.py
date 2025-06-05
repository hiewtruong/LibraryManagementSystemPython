from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QGridLayout, QMessageBox, QDateEdit,
    QHeaderView, QSizePolicy, QGroupBox
)
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QColor
from datetime import datetime
from domain.dto.transaction.transaction_loan_header_request_dto import TransactionLoanHeaderRequestDTO
from domain.dto.transaction.transaction_loan_detail_request_dto import TransactionLoanDetailRequestDTO
from lib.common_ui.confirm_modal import ConfirmModal
from lib.date_utils import format_date_yyyy, is_valid_return_date
from lib.notifier_utils import show_success, show_warning
from views.transactions_loan.choose_user_transaction_dialog import TransactionUserChooseModal

class CreateTransactionLoanPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: white;")
        self.parent = parent
        self.controller = None 
        self.users = []
        self.all_books = []
        self.setMinimumSize(1370, 830)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.selected_books = []
        self.transaction_request_dto = TransactionLoanHeaderRequestDTO()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 10, 10)
        main_layout.setSpacing(5)
        
        title_label = QLabel("Create Transaction Loan")
        title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            border: none;
            padding-top: 10px;
            background-color: none;
        """)
        title_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(title_label)

        top_panel = QWidget()
        top_panel.setContentsMargins(0, 10, 0, 0)
        top_layout = QHBoxLayout(top_panel)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)
        top_layout.setAlignment(Qt.AlignLeft) 

        left_panel = QWidget()
        left_panel.setContentsMargins(0, 0, 0, 0)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setAlignment(Qt.AlignLeft)

        user_panel = QWidget()
        user_panel.setContentsMargins(0, 0, 0, 0)
        user_layout = QHBoxLayout(user_panel)
        user_layout.setContentsMargins(0, 0, 0, 0)
        user_layout.setSpacing(5)

        user_label = QLabel("User:")
        user_label_font = QFont()
        user_label_font.setPixelSize(13)
        user_label_font.setBold(True)
        user_label.setFont(user_label_font)
        user_label.setStyleSheet("border: none;")  
        user_layout.addWidget(user_label)

        self.lbl_user_prompt = QLabel("Please Choose User")
        lbl_user_prompt_font = QFont()
        lbl_user_prompt_font.setPixelSize(12)
        self.lbl_user_prompt.setFont(lbl_user_prompt_font)
        self.lbl_user_prompt.setStyleSheet("border: none;")
        user_layout.addWidget(self.lbl_user_prompt)

        self.lbl_selected_user = QLabel("")
        lbl_selected_user_font = QFont()
        lbl_selected_user_font.setPixelSize(12)
        self.lbl_selected_user.setFont(lbl_selected_user_font)
        self.lbl_selected_user.setStyleSheet("border: none;") 
        user_layout.addWidget(self.lbl_selected_user)

        btn_choose_user = QPushButton("Choose")
        btn_choose_user.setFixedSize(80, 25)
        btn_choose_user.setStyleSheet("""
            background-color: #ffda33;
            color: white;
            border-radius: 5px;
        """)
        btn_choose_user.clicked.connect(self.open_user_selection_dialog)
        user_layout.addWidget(btn_choose_user)

        user_layout.addStretch()

        btn_save = QPushButton("CREATE")
        btn_save.setFixedSize(90, 30)
        btn_save.setStyleSheet("""
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            font-size: 13px;
            font-weight: bold;
        """)
        btn_save.clicked.connect(self.save_transaction)
        user_layout.addWidget(btn_save)

        left_layout.addWidget(user_panel)

        date_panel = QWidget()
        date_panel.setContentsMargins(0, 4, 0, 0)
        date_layout = QHBoxLayout(date_panel)
        date_layout.setContentsMargins(0, 4, 0, 0)

        date_label = QLabel("Loan Return Date:")
        date_label_font = QFont()
        date_label_font.setPixelSize(13)
        date_label_font.setBold(True)
        date_label.setFont(date_label_font)
        date_label.setStyleSheet("border: none;") 
        date_layout.addWidget(date_label)

        self.loan_return_dt_field = QDateEdit()
        loan_return_dt_field_font = QFont()
        loan_return_dt_field_font.setPixelSize(12)
        self.loan_return_dt_field.setFont(loan_return_dt_field_font)
        self.loan_return_dt_field.setFixedSize(150, 25)
        self.loan_return_dt_field.setCalendarPopup(True)
        self.loan_return_dt_field.setDisplayFormat("MM/dd/yyyy")
        self.loan_return_dt_field.setDate(QDate.currentDate())
        date_layout.addWidget(self.loan_return_dt_field)

        date_layout.addStretch()
        left_layout.addWidget(date_panel)

        total_qty_panel = QWidget()
        total_qty_panel.setContentsMargins(0, 7, 0, 0)
        total_qty_layout = QHBoxLayout(total_qty_panel)
        total_qty_layout.setContentsMargins(0, 7, 0, 0)
        total_qty_label = QLabel("Total Quantity:")
        total_qty_label_font = QFont()
        total_qty_label_font.setPixelSize(13)
        total_qty_label_font.setBold(True)
        total_qty_label.setFont(total_qty_label_font)
        total_qty_label.setStyleSheet("border: none;")
        total_qty_layout.addWidget(total_qty_label)

        self.lbl_total_quantity = QLabel("0")
        lbl_total_quantity_font = QFont()
        lbl_total_quantity_font.setPixelSize(12)
        self.lbl_total_quantity.setFont(lbl_total_quantity_font)
        self.lbl_total_quantity.setStyleSheet("border: none;")
        total_qty_layout.addWidget(self.lbl_total_quantity)

        total_qty_layout.addStretch()
        left_layout.addWidget(total_qty_panel)

        top_layout.addWidget(left_panel)

        main_layout.addWidget(top_panel)

        tables_panel = QWidget()
        tables_panel.setContentsMargins(0, 10, 0, 0)
        tables_layout = QGridLayout(tables_panel)
        tables_layout.setContentsMargins(0, 10, 0, 0)

        available_books_group = QGroupBox("Available Books")
        available_books_group_font = QFont()
        available_books_group_font.setPixelSize(15)
        available_books_group_font.setBold(True)
        available_books_group.setFont(available_books_group_font)
        available_books_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 3px;
            }
        """)
        available_books_layout = QVBoxLayout(available_books_group)
        available_books_layout.setContentsMargins(10, 10, 10, 10) 
        available_books_layout.setAlignment(Qt.AlignLeft)

        search_panel = QWidget()
        search_layout = QHBoxLayout(search_panel)
        search_label = QLabel("Search by Title:")
        search_label_font = QFont()
        search_label_font.setPixelSize(13)
        search_label_font.setBold(True)
        search_label.setFont(search_label_font)
        search_label.setStyleSheet("border: none;") 
        search_layout.addWidget(search_label)

        self.search_field = QLineEdit()
        search_field_font = QFont()
        search_field_font.setPixelSize(13)
        self.search_field.setFont(search_field_font)
        self.search_field.setFixedSize(150, 25) 
        self.search_field.setPlaceholderText("Enter Key Word")
        self.search_field.textChanged.connect(self.perform_search)
        search_layout.addWidget(self.search_field)

        search_layout.addStretch()

        btn_refresh = QPushButton("Refresh")
        btn_refresh.setFixedSize(70, 25)
        btn_refresh.setStyleSheet("""
            background-color: #4bf540;
            color: white;
            border-radius: 5px;
            font-size: 13px;
            font-weight: bold;
        """)
        btn_refresh.clicked.connect(self.refresh_available_books)
        search_layout.addWidget(btn_refresh)
        available_books_layout.addWidget(search_panel)

        self.available_books_table = QTableWidget()
        self.available_books_table.verticalHeader().setVisible(False)
        self.available_books_table.setColumnCount(6)
        self.available_books_table.setHorizontalHeaderLabels(["Book ID", "Title", "Author", "Genre", "Publisher", "Publish Year"])
        self.available_books_table.setFont(QFont("Arial", 12))
        header_font = QFont()
        header_font.setPixelSize(13)
        header_font.setBold(True)
        for i in range(self.available_books_table.columnCount()):
            header_item = self.available_books_table.horizontalHeaderItem(i)
            if header_item:
                header_item.setFont(header_font)
        self.available_books_table.setRowHeight(0, 20)
        self.available_books_table.setShowGrid(True)
        self.available_books_table.setStyleSheet("""
            QTableWidget {
                gridline-color: lightgray;
                background-color: #f9f9f9;
                selection-background-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 2px;
            }
        """)
        self.available_books_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.available_books_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.available_books_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.available_books_table.setColumnWidth(0, 80)
        self.available_books_table.setColumnWidth(1, 300)
        self.available_books_table.setColumnWidth(2, 150)
        self.available_books_table.setColumnWidth(3, 200)
        self.available_books_table.setColumnWidth(4, 150)
        self.available_books_table.setColumnWidth(5, 150)
        self.available_books_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        available_books_layout.addWidget(self.available_books_table)

        tables_layout.addWidget(available_books_group, 0, 0, 1, 1)

        button_panel = QWidget()
        button_layout = QVBoxLayout(button_panel)
        button_layout.setAlignment(Qt.AlignCenter)

        btn_move = QPushButton("Move")
        btn_move.setFont(QFont("Arial", 13, QFont.Bold))
        btn_move.clicked.connect(self.move_book_to_selected)
        button_layout.addWidget(btn_move)

        btn_remove = QPushButton("Remove")
        btn_remove.setFont(QFont("Arial", 13, QFont.Bold))
        btn_remove.clicked.connect(self.move_book_to_available)
        button_layout.addWidget(btn_remove)

        tables_layout.addWidget(button_panel, 0, 1, 1, 1)

        selected_books_group = QGroupBox("Selected Books")
        selected_books_group_font = QFont()
        selected_books_group_font.setPixelSize(15)
        selected_books_group_font.setBold(True)
        selected_books_group.setFont(selected_books_group_font)
        selected_books_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 3px;
            }
        """)
        selected_books_layout = QVBoxLayout(selected_books_group)
        selected_books_layout.setContentsMargins(10, 10, 10, 10)
        selected_books_layout.setAlignment(Qt.AlignRight)

        search_selected_panel = QWidget()
        search_selected_layout = QHBoxLayout(search_selected_panel)
        search_selected_label = QLabel("Search by Title:")
        search_selected_label_font = QFont()
        search_selected_label_font.setPixelSize(13)
        search_selected_label_font.setBold(True)
        search_selected_label.setFont(search_selected_label_font)
        search_selected_label.setStyleSheet("border: none;")
        search_selected_layout.addWidget(search_selected_label)

        self.search_field_selected = QLineEdit()
        search_selected_label_font = QFont()
        search_selected_label_font.setPixelSize(13)
        self.search_field_selected.setFont(search_selected_label_font)
        self.search_field_selected.setFixedSize(150, 25)
        self.search_field_selected.setPlaceholderText("Enter Key Word") 
        self.search_field_selected.textChanged.connect(self.perform_search_selected)
        search_selected_layout.addWidget(self.search_field_selected)

        search_selected_layout.addStretch()

        btn_refresh_selected = QPushButton("Refresh")
        btn_refresh_selected.setFixedSize(70, 25)
        btn_refresh_selected.setStyleSheet("""
            background-color: #4bf540;
            color: white;
            border-radius: 5px;
            font-size: 13px;
            font-weight: bold;
        """)
        btn_refresh_selected.clicked.connect(self.refresh_selected_books)
        search_selected_layout.addWidget(btn_refresh_selected)
        selected_books_layout.addWidget(search_selected_panel)

        self.selected_books_table = QTableWidget()
        self.selected_books_table.verticalHeader().setVisible(False)
        self.selected_books_table.setColumnCount(6)
        self.selected_books_table.setHorizontalHeaderLabels(["Book ID", "Title", "Author", "Genre", "Publisher", "Publish Year"])
        self.selected_books_table.setFont(QFont("Arial", 13))
        header_font = QFont()
        header_font.setPixelSize(13)
        header_font.setBold(True)
        for i in range(self.selected_books_table.columnCount()):
            header_item = self.selected_books_table.horizontalHeaderItem(i)
            if header_item:
                header_item.setFont(header_font)
        self.selected_books_table.setRowHeight(0, 20)
        self.selected_books_table.setShowGrid(True)
        self.selected_books_table.setStyleSheet("""
            QTableWidget {
                gridline-color: lightgray;
                background-color: #f9f9f9;
                selection-background-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 2px;
            }
        """)
        self.selected_books_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.selected_books_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.selected_books_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.selected_books_table.setColumnWidth(0, 80)
        self.selected_books_table.setColumnWidth(1, 300)
        self.selected_books_table.setColumnWidth(2, 150)
        self.selected_books_table.setColumnWidth(3, 200)
        self.selected_books_table.setColumnWidth(4, 150)
        self.selected_books_table.setColumnWidth(5, 150)
        self.selected_books_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        selected_books_layout.addWidget(self.selected_books_table)

        tables_layout.addWidget(selected_books_group, 0, 2, 1, 1)

        tables_layout.setColumnStretch(0, 1)
        tables_layout.setColumnStretch(1, 0)
        tables_layout.setColumnStretch(2, 1)
        main_layout.addWidget(tables_panel)

    def load_data(self):
        if self.controller:
            self.all_books = self.controller.get_all_books()
            self.users = self.controller.get_all_users()
            self.refresh_available_books()

    def update_total_quantity(self):
        self.lbl_total_quantity.setText(str(len(self.selected_books)))
        self.transaction_request_dto.total_qty = len(self.selected_books)

    def perform_search(self):
        keyword = self.search_field.text().strip().lower()
        self.available_books_table.setRowCount(0)
        data_font = QFont()
        data_font.setPixelSize(12)

        for book in self.all_books:
            if book not in self.selected_books:
                if not keyword or keyword in book.title.lower():
                    row = self.available_books_table.rowCount()
                    self.available_books_table.insertRow(row)
                    items = [
                        QTableWidgetItem(str(book.book_id)),
                        QTableWidgetItem(book.title),
                        QTableWidgetItem(book.author),
                        QTableWidgetItem(book.genre_category),
                        QTableWidgetItem(book.publisher),
                        QTableWidgetItem(format_date_yyyy(book.publish_year))
                    ]
                    for col_idx, item in enumerate(items):
                        self.available_books_table.setItem(row, col_idx, item)
                        item.setFont(data_font)
                    if book.is_out_of_stock:
                        for col in range(6):
                            item = self.available_books_table.item(row, col)
                            if item:
                                item.setForeground(QColor("red"))

    def perform_search_selected(self):
        keyword = self.search_field_selected.text().strip().lower()
        self.selected_books_table.setRowCount(0)
        data_font = QFont()
        data_font.setPixelSize(12)

        for book in self.selected_books:
            if not keyword or keyword in book.title.lower():
                row = self.selected_books_table.rowCount()
                self.selected_books_table.insertRow(row)
                items = [
                    QTableWidgetItem(str(book.book_id)),
                    QTableWidgetItem(book.title),
                    QTableWidgetItem(book.author),
                    QTableWidgetItem(book.genre_category),
                    QTableWidgetItem(book.publisher),
                    QTableWidgetItem(format_date_yyyy(book.publish_year))
                ]
                for col_idx, item in enumerate(items):
                    self.selected_books_table.setItem(row, col_idx, item)
                    item.setFont(data_font)

    def refresh_available_books(self):
        self.search_field.setText("")
        self.available_books_table.setRowCount(0)
        data_font = QFont()
        data_font.setPixelSize(12)

        for book in self.all_books:
            if book not in self.selected_books:
                row = self.available_books_table.rowCount()
                self.available_books_table.insertRow(row)
                items = [
                    QTableWidgetItem(str(book.book_id)),
                    QTableWidgetItem(book.title),
                    QTableWidgetItem(book.author),
                    QTableWidgetItem(book.genre_category),
                    QTableWidgetItem(book.publisher),
                    QTableWidgetItem(format_date_yyyy(book.publish_year))
                ]
                for col_idx, item in enumerate(items):
                    self.available_books_table.setItem(row, col_idx, item)
                    item.setFont(data_font)
                if book.is_out_of_stock:
                    for col in range(6):
                        item = self.available_books_table.item(row, col)
                        if item:
                            item.setForeground(QColor("red"))

    def refresh_selected_books(self):
        self.search_field_selected.setText("")
        self.selected_books_table.setRowCount(0)
        data_font = QFont()
        data_font.setPixelSize(12)

        for book in self.selected_books:
            row = self.selected_books_table.rowCount()
            self.selected_books_table.insertRow(row)
            items = [
                QTableWidgetItem(str(book.book_id)),
                QTableWidgetItem(book.title),
                QTableWidgetItem(book.author),
                QTableWidgetItem(book.genre_category),
                QTableWidgetItem(book.publisher),
                QTableWidgetItem(format_date_yyyy(book.publish_year))
            ]
            for col_idx, item in enumerate(items):
                self.selected_books_table.setItem(row, col_idx, item)
                item.setFont(data_font)
        self.update_total_quantity()

    def open_user_selection_dialog(self):
        selected_user = self.controller.choose_user_create_trans(self, self.users)
        if selected_user:
            self.lbl_selected_user.setText(selected_user.user_name)
            self.lbl_user_prompt.setText("")
            self.transaction_request_dto.user_id = selected_user.user_id

    def save_transaction(self):
        if not self.lbl_selected_user.text():
            show_warning(parent=self.parent ,message="Please choose a user.")
            return

        return_date = self.parse_loan_return_date()
        if not return_date:
            show_warning(parent=self.parent ,message="Please enter a correct date format (MM/dd/YYYY).")
            return

        self.transaction_request_dto.loan_return_dt = return_date

        if is_valid_return_date(return_date) == False:
            show_warning(parent=self.parent ,message="Return date must be at least 1 day after today.")
            return

        if not self.selected_books:
            show_warning(parent=self.parent ,message="Please select at least one book.")
            return

        loan_details = []
        for book in self.selected_books:
            detail = TransactionLoanDetailRequestDTO()
            detail.load_book_id = book.book_id
            loan_details.append(detail)
        self.transaction_request_dto.loan_details = loan_details

        modal = ConfirmModal(self, message="Are you sure you want to create this transaction?", title="Confirm")
        if modal.exec_() == QtWidgets.QDialog.Accepted:
            try:
                if self.controller:
                    header_id = self.controller.create_transaction_loan(self.transaction_request_dto)
                    self.controller.send_email_create_transaction_loan(header_id)
                    show_success(parent=self.parent,message="Transaction created successfully!")
                    self.reset_form()
                    if self.controller:
                        self.controller.show_transaction_loan_panel()
            except Exception as ex:
                QMessageBox.critical(self, "Error", f"Failed to create transaction: {str(ex)}")

           
    def parse_loan_return_date(self):
        try:
            date_str = self.loan_return_dt_field.text()
            return datetime.strptime(date_str, "%m/%d/%Y")
        except ValueError:
            return None

    def move_book_to_selected(self):
        selected_row = self.available_books_table.currentRow()
        if selected_row == -1:
            show_warning(parent=self.parent ,message="Please select a book to move.")
            return

        book_id = int(self.available_books_table.item(selected_row, 0).text())
        book = next((b for b in self.all_books if b.book_id == book_id), None)
        if book and book.is_out_of_stock:
            show_warning(parent=self.parent,message="This book is out of stock.")
            return

        self.selected_books.append(book)
        self.available_books_table.removeRow(selected_row)
        self.refresh_selected_books()
        self.perform_search()

    def move_book_to_available(self):
        selected_row = self.selected_books_table.currentRow()
        if selected_row == -1:
            show_warning(parent=self.parent,message="Please select a book to remove.")
            return

        book_id = int(self.selected_books_table.item(selected_row, 0).text())
        book = next((b for b in self.selected_books if b.book_id == book_id), None)
        if book:
            self.selected_books.remove(book)
        self.selected_books_table.removeRow(selected_row)
        self.refresh_available_books()
        self.perform_search_selected()

    def reset_form(self):
        self.lbl_selected_user.setText("")
        self.lbl_user_prompt.setText("Please Choose User")
        self.loan_return_dt_field.setDate(QDate.currentDate())
        self.selected_books.clear()
        self.refresh_available_books()
        self.refresh_selected_books()
        self.transaction_request_dto = TransactionLoanHeaderRequestDTO()