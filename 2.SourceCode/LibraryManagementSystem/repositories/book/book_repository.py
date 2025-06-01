import pyodbc
from typing import List
from db_utils import get_connection, close
from domain.dto.transaction.transaction_loan_detail_request_dto import TransactionLoanDetailRequestDTO
from domain.entities.book import Book
from repositories.book.i_book_repository import IBookRepository

class BookRepository(IBookRepository):
    _instance = None

    @staticmethod
    def get_instance():
        if BookRepository._instance is None:
            BookRepository._instance = BookRepository()
        return BookRepository._instance

    def get_all_books(self) -> List[Book]:
        books = []
        sql = """
            SELECT * FROM Books
            WHERE IsDelete = 0
            ORDER BY BookID DESC
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                book = Book.from_row(row)
                books.append(book)
        except Exception as e:
            print(f"Error fetching books: {e}")
        finally:
            close()
        return books

    def update_qty_allocated(self, loan_details: List[TransactionLoanDetailRequestDTO],conn=None) -> None:
        sql = "UPDATE Books SET QtyAllocated = QtyAllocated + 1 WHERE BookID = ?"
        if conn is None:
            conn = get_connection()
        try:
            cursor = conn.cursor()
            for detail in loan_details:
                cursor.execute(sql, (detail.load_book_id))
            conn.commit()
        except Exception as e:
            print(f"Error updating QtyAllocated: {e}")

    def decrement_qty_allocated(self, loan_details: list[TransactionLoanDetailRequestDTO], conn=None) -> None:
        sql = "UPDATE Books SET QtyAllocated = QtyAllocated - 1 WHERE BookID = ?"
        if conn is None:
            conn = get_connection()
        try:
            cursor = conn.cursor()
            for detail in loan_details:
                cursor.execute(sql, (detail.load_book_id))
        except Exception as e:
            print(f"Error decrementing QtyAllocated: {e}")
            raise 
