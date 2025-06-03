from typing import List
from PyQt5.QtWidgets import QWidget
from domain.dto.book.book_dto import BookDTO
from domain.dto.transaction.transaction_loan_header_dto import TransactionLoanHeaderDTO
from domain.dto.transaction.transaction_loan_header_request_dto import TransactionLoanHeaderRequestDTO
from domain.dto.transaction.transaction_loan_header_revoke_dto import TransactionLoanHeaderRevokeDTO
from domain.dto.user.user_dto import UserDTO
from domain.dto.user.user_role_dto import UserRoleDTO
from services.book.book_service import BookService
from services.user.user_service import UserService
from views.transactions_loan.choose_user_transaction_dialog import TransactionUserChooseModal
from views.transactions_loan.transaction_detail_dialog import TransactionLoanDetailDialog
from views.transactions_loan.transaction_loan_panel import TransactionLoanPanel
from services.transaction_loan.transaction_loan_service import TransactionLoanService

class TransactionLoanController:
    def __init__(self, dashboard=None):
        self.trans_service = TransactionLoanService.get_instance()
        self.book_service = BookService.get_instance()
        self.user_service = UserService.get_instance()
        self.dashboard = dashboard

    def get_all_transaction_headers(self, filter_user_name: str = "", filter_status: str = ""):
        return self.trans_service.get_all_transaction_headers(filter_user_name, filter_status)

    def get_transaction_details(self, loan_header_id: int):
        return self.trans_service.get_transaction_details(loan_header_id)

    def revoke_transaction(self, request: TransactionLoanHeaderRevokeDTO):
        is_success: bool = False
        try:
            self.trans_service.revoke_transaction(request)
            is_success = True
        except Exception as e:
            print(f"Error revoking transaction: {e}")
            is_success = False
        finally:
            return is_success

    def view_transaction_detail(self, parent: QWidget, container: QWidget, header_dto: TransactionLoanHeaderDTO):
        details = self.trans_service.get_transaction_details(header_dto.loan_header_id)
        dialog = TransactionLoanDetailDialog(parent, container, header_dto, details)
        dialog.reloadDataSignal.connect(self.on_dialog_reload)
        dialog.exec_()

    def on_dialog_reload(self):
        if self.dashboard and hasattr(self.dashboard, 'current_panel'):
            panel = self.dashboard.current_panel
            if isinstance(panel, TransactionLoanPanel):
                panel.load_data()

    def load_transaction_headers(self, panel):
        if panel:
            headers = self.get_all_transaction_headers()
            panel.update_table(headers)

    def search_transaction_headers(self, panel, keyword: str, column: str):
        headers = self.trans_service.get_all_transaction_headers(keyword, column)
        panel.update_search_table(headers)

    def show_transaction_loan_panel(self):
        if self.dashboard:
            self.dashboard.show_transaction_loan_panel()

    def get_all_books(self) -> List[BookDTO]:
       books = self.book_service.get_all_book_trans()
       return books
        
    def get_all_users(self) -> List[UserRoleDTO]:
         users = self.user_service.get_all_users_customer()
         return users

    def choose_user_create_trans(self, parent: QWidget, list_user: List[UserRoleDTO]):
        dialog = TransactionUserChooseModal(parent, list_user)
        dialog.exec_()
        selected_user = dialog.get_selected_user()
        return selected_user

    def call_back_create_trans(self):
        if self.dashboard and hasattr(self.dashboard, 'current_panel'):
            panel = self.dashboard.current_panel

    def create_transaction_loan(self, request:TransactionLoanHeaderRequestDTO)-> int :
        header_id = self.trans_service.create_transaction(request=request)
        return header_id

    def send_email_create_transaction_loan(self, header_id :int)-> None :
         self.trans_service.send_email_transaction(header_id)
    
    def send_email_revoke_transaction_loan(self, header_id :int)-> None :
         self.trans_service.send_email_revoke_transaction(header_id)
    
    def send_email_remind_transaction_loan(self, header_id :int)-> None :
         self.trans_service.send_email_remind_transaction(header_id)