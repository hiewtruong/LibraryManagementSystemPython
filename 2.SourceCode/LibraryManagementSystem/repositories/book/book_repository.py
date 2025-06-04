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

    def add_book(self, book: Book) -> Book:
        sql = """
            INSERT INTO Books (Title, Author, Cover, LandingPage, Hashtag, GenreCategory, Publisher, PublishYear, Location, IsDisplay, QtyOH, QtyAllocated, CreatedBy, UpdateBy, IsDelete, CreatedDt, UpdateDt)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0, ?, ?, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (
                book.title, book.author, book.cover, book.landing_page, book.hashtag,
                book.genre_category, book.publisher, book.publish_year, book.location,
                book.is_display, book.created_by, book.update_by
            ))
            conn.commit()
            cursor.execute("SELECT SCOPE_IDENTITY()")
            book_id = cursor.fetchone()[0]
            book.set_book_id(book_id)
            return book
        except Exception as e:
            print(f"Error adding book: {e}")
            raise
        finally:
            close()

    def update_book(self, book: Book) -> Book:
        sql = """
            UPDATE Books
            SET Title = ?, Author = ?, Cover = ?, LandingPage = ?, Hashtag = ?, GenreCategory = ?, Publisher = ?, PublishYear = ?, Location = ?, IsDisplay = ?, UpdateBy = ?
            WHERE BookID = ?
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (
                book.title, book.author, book.cover, book.landing_page, book.hashtag,
                book.genre_category, book.publisher, book.publish_year, book.location,
                book.is_display, book.update_by, book.book_id
            ))
            conn.commit()
            return book
        except Exception as e:
            print(f"Error updating book: {e}")
            raise
        finally:
            close()

    def delete_book(self, book_id: int) -> bool:
        sql = "UPDATE Books SET IsDelete = 1 WHERE BookID = ?"
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (book_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting book: {e}")
            return False
        finally:
            close()

    def get_book_by_id(self, book_id: int) -> Book:
        sql = "SELECT * FROM Books WHERE BookID = ? AND IsDelete = 0"
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (book_id,))
            row = cursor.fetchone()
            if row:
                return Book.from_row(row)
            return None
        except Exception as e:
            print(f"Error fetching book by ID: {e}")
            return None
        finally:
            close()