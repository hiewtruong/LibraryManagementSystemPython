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

    @abstractmethod
    def add_book(self, book: Book) -> Book:
        pass

    @abstractmethod
    def update_book(self, book: Book):
        pass

    @abstractmethod
    def delete_book(self, book_id: int):
        pass

    @abstractmethod
    def get_book_by_id(self, book_id: int) -> Book:
        pass