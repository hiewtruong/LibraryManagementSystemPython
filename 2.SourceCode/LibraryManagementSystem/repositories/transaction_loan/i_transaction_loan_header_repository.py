# repositories/transaction_loan_header/i_transaction_loan_header_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.dto.transaction.transaction_loan_header_dto import TransactionLoanHeaderDTO
from domain.dto.transaction.transaction_loan_header_request_dto import TransactionLoanHeaderRequestDTO
from domain.entities.transaction_loan_header import TransactionLoanHeader

class ITransactionLoanHeaderRepository(ABC):

    @abstractmethod
    def get_all_trans_headers(self) -> List[TransactionLoanHeaderDTO]:
        pass

    @abstractmethod
    def get_all_trans_headers_by_keyword(self, keyword: str, column: str) -> List[TransactionLoanHeaderDTO]:
        pass

    @abstractmethod
    def create_transaction_loan_header(self, request_dto: TransactionLoanHeaderRequestDTO) -> int:
        pass

    @abstractmethod
    def update_status_revoke(self, loan_header_id: int) -> None:
        pass

    @abstractmethod
    def find_trans_header_loan(self, loan_header_id: int) -> Optional[TransactionLoanHeader]:
        pass
