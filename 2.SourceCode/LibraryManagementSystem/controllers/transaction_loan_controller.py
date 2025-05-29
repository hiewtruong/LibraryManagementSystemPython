from typing import List
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QDialog
from services.transaction_loan.transaction_loan_service import TransactionLoanService
from services.user.user_service import UserService
from services.book.book_service import BookService
from domain.dto.transaction.transaction_loan_header_request_dto import TransactionLoanHeaderRequestDTO
from domain.dto.transaction.transaction_loan_detail_request_dto import TransactionLoanDetailRequestDTO
from domain.dto.user.user_dto import UserDTO
from domain.dto.book.book_dto import BookDTO
from views.transaction.create_transaction_panel import CreateTransactionLoanPanel
from views.transaction.transaction_panel import TransactionLoanPanel
from views.transaction.view_transaction_detail_modal import ViewTransactionLoanDetailModal
from views.transaction.choose_user_modal import TransactionUserChooseModal


class TransactionLoanController:
    def __init__(self):
        self.trans_service = TransactionLoanService.get_instance()
        self.user_service = UserService.get_instance()
        self.book_service = BookService.get_instance()

    def init_transaction_list(self, container: QWidget, force_reload=False):
        if force_reload or not (container.layout() and isinstance(container.layout().itemAt(0).widget(), TransactionLoanPanel)):
            layout = QVBoxLayout()
            container.setLayout(layout)
            data = self.trans_service.get_all_transaction_headers()
            panel = TransactionLoanPanel(data, container)
            layout.addWidget(panel)

    def create_transaction_panel(self, container: QWidget, force_reload=False):
        if force_reload or not (container.layout() and isinstance(container.layout().itemAt(0).widget(), CreateTransactionLoanPanel)):
            layout = QVBoxLayout()
            container.setLayout(layout)
            users = self.user_service.get_all_users()
            books = self.book_service.get_all_books_for_transaction()
            panel = CreateTransactionLoanPanel(container, users, books)
            layout.addWidget(panel)

    def view_transaction_detail(self, parent: QWidget, container: QWidget, header_dto):
        details = self.trans_service.get_transaction_details(header_dto.loan_header_id)
        dialog = ViewTransactionLoanDetailModal(parent, container, header_dto, details)
        dialog.exec_()

    def choose_user_modal(self, parent: QWidget, container: QWidget, users: List[UserDTO]):
        dialog = TransactionUserChooseModal(parent, container, users)
        dialog.exec_()

    def rent_books_from_cart(self, user: UserDTO, books: List[BookDTO]):
        if user is None:
            raise ValueError("User must be logged in.")
        if not books:
            raise ValueError("No books selected.")

        header = TransactionLoanHeaderRequestDTO()
        header.user_id = user.user_id
        header.total_qty = len(books)

        from datetime import datetime, timedelta
        header.loan_return_dt = datetime.now() + timedelta(days=7)

        details = []
        for book in books:
            detail = TransactionLoanDetailRequestDTO()
            detail.load_book_id = book.book_id
            details.append(detail)

        header.loan_details = details
        self.trans_service.create_transaction(header)
