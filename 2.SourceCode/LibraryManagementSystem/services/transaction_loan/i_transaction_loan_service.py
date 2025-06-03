# services/transaction_loan/i_transaction_loan_service.py
from abc import ABC, abstractmethod
from typing import List
from domain.dto.transaction.transaction_loan_header_dto import TransactionLoanHeaderDTO
from domain.dto.transaction.transaction_loan_detail_dto import TransactionLoanDetailDTO
from domain.dto.transaction.transaction_loan_header_request_dto import TransactionLoanHeaderRequestDTO
from domain.dto.transaction.transaction_loan_header_revoke_dto import TransactionLoanHeaderRevokeDTO

class ITransactionLoanService(ABC):

    @abstractmethod
    def get_all_transaction_loan_headers_by_keyword(self, keyword: str, column: str) -> List[TransactionLoanHeaderDTO]:
        pass

    @abstractmethod
    def get_all_transaction_loan_details(self, loan_header_id: int) -> List[TransactionLoanDetailDTO]:
        pass

    @abstractmethod
    def create_transaction_loan(self, request: TransactionLoanHeaderRequestDTO) -> int:
        pass

    @abstractmethod
    def revoke_transaction_loan(self, request: TransactionLoanHeaderRevokeDTO) -> None:
        pass

    @abstractmethod
    def send_email_transaction(self, loan_header_id: int) -> None:
        pass

    @abstractmethod
    def send_email_revoke_transaction(self, loan_header_id: int) -> None:
        pass

    @abstractmethod
    def send_email_remind_transaction(self, loan_header_id: int) -> None:
        pass