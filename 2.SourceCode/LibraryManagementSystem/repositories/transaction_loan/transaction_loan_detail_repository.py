# repositories/transaction_loan_detail/transaction_loan_detail_repository.py
from time import localtime, strftime
from typing import List
from domain.dto.transaction.transaction_loan_detail_dto import TransactionLoanDetailDTO
from domain.dto.transaction.transaction_loan_detail_request_dto import TransactionLoanDetailRequestDTO
from repositories.transaction_loan.i_transaction_loan_detail_repository import ITransactionLoanDetailRepository
from db_utils import get_connection, close
from lib.constants import ADMIN
import datetime

class TransactionLoanDetailRepository(ITransactionLoanDetailRepository):
    def get_transaction_loans_by_header_id(self, loan_header_id: int) -> List[TransactionLoanDetailDTO]:
        result: List[TransactionLoanDetailDTO] = []
        sql = """
            SELECT T.LoanDetailID, T.LoanHeaderID, T.LoanBookID, T.CreatedBy, T.CreatedDt, T.UpdateBy, T.UpdateDt,
                   B.BookID, B.Title, B.Author, B.GenreCategory, B.Publisher, B.PublishYear
            FROM TransactionLoanDetails AS T
            INNER JOIN Books AS B ON T.LoanBookID = B.BookID
            WHERE T.IsDelete = 0 AND T.LoanHeaderID = ?
        """
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (loan_header_id,))
            rows = cursor.fetchall()
            for row in rows:
                dto = TransactionLoanDetailDTO(
                    loan_detail_id=row[0],
                    loan_header_id=row[1],
                    loan_book_id=row[2],
                    created_by=row[3],
                    created_dt=row[4],
                    update_by=row[5],
                    update_dt=row[6],
                    book_id=row[7],
                    title=row[8],
                    author=row[9],
                    genre_category=row[10],
                    publisher=row[11],
                    publish_year=row[12]
                )
                result.append(dto)
        except Exception as e:
            raise Exception(f"[TransactionLoanDetailRepository.get_transaction_loans_by_header_id] {str(e)}")
        finally:
            close()
        return result

    def create_transaction_loan_details(self, header_id: int, loan_details: List[TransactionLoanDetailRequestDTO],conn=None) -> None:
        sql = """
            INSERT INTO TransactionLoanDetails 
            (LoanHeaderID, LoanBookID, CreatedDt, CreatedBy, UpdateDt, UpdateBy, IsDelete)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        if conn is None:
            conn = get_connection()
        try:
            cursor = conn.cursor()
            now = localtime()
            for detail in loan_details:
                cursor.execute(sql, (
                    header_id,
                    detail.load_book_id,
                    strftime("%Y-%m-%d %H:%M:%S", now),
                    ADMIN,
                    strftime("%Y-%m-%d %H:%M:%S", now),
                    ADMIN,
                    0
                ))
        except Exception as e:
            print(f"Error create_transaction_loan_details: {e}")
            raise
