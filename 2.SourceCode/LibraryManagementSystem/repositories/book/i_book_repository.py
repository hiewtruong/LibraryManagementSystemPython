from abc import ABC, abstractmethod
from typing import List
from domain.dto.transaction.transaction_loan_detail_request_dto import TransactionLoanDetailRequestDTO
from domain.entities.book import Book

class IBookRepository(ABC):
    @abstractmethod
    def get_all_books(self) -> List[Book]:
        pass

    @abstractmethod
    def update_qty_allocated(self, loan_details: List[TransactionLoanDetailRequestDTO],conn=None) -> None:
        pass

    @abstractmethod
    def decrement_qty_allocated(self, loan_details: List[TransactionLoanDetailRequestDTO],conn=None) -> None:
        pass