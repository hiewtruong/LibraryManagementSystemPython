# repositories/transaction_loan_detail/i_transaction_loan_detail_repository.py
from abc import ABC, abstractmethod
from typing import List
from domain.dto.transaction.transaction_loan_detail_dto import TransactionLoanDetailDTO
from domain.dto.transaction.transaction_loan_detail_request_dto import TransactionLoanDetailRequestDTO

class ITransactionLoanDetailRepository(ABC):

    @abstractmethod
    def get_transaction_loans_by_header_id(self, loan_header_id: int) -> List[TransactionLoanDetailDTO]:
        pass

    @abstractmethod
    def create_transaction_loan_details(self, header_id: int, loan_details: List[TransactionLoanDetailRequestDTO]) -> None:
        pass
