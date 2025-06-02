from time import localtime, strftime
from typing import List, Optional
import datetime  
from db_utils import get_connection, close
from domain.dto.transaction.transaction_loan_header_dto import TransactionLoanHeaderDTO
from domain.dto.transaction.transaction_loan_header_request_dto import TransactionLoanHeaderRequestDTO
from domain.entities.transaction_loan_header import TransactionLoanHeader
from lib.constants import ADMIN
from repositories.transaction_loan.i_transaction_loan_header_repository import ITransactionLoanHeaderRepository

class TransactionLoanHeaderRepository(ITransactionLoanHeaderRepository):
    def __init__(self):
        self.db = get_connection()

    def get_all_trans_headers(self) -> List[TransactionLoanHeaderDTO]:
        query = '''
        SELECT T.LoanHeaderID, T.LoanTicketNumber, T.UserID_FK, 
               U.UserName, U.Email, U.Phone, 
               T.TotalQty, T.LoanDt, T.LoanReturnDt, 
               T.CreatedBy, T.CreatedDt, T.UpdateBy, T.UpdateDt, T.Status
        FROM TransactionLoanHeaders T
        JOIN Users U ON T.UserID_FK = U.UserID
        WHERE T.IsDelete = 0
        ORDER BY T.LoanHeaderID DESC
        '''
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        result = []
        for row in rows:
            dto = TransactionLoanHeaderDTO(
                loan_header_id=row[0],
                loan_ticket_number=row[1],
                user_id=row[2],
                use_name=row[3],
                email=row[4],
                phone=row[5],
                total_qty=row[6],
                loan_dt=row[7],
                loan_return_dt=row[8],
                created_by=row[9],
                created_dt=row[10],
                update_by=row[11],
                update_dt=row[12],
                status=row[13]
            )
            result.append(dto)
        return result

    def get_all_trans_headers_by_keyword(self, keyword: str, column: str) -> List[TransactionLoanHeaderDTO]:
        query = f'''
        SELECT T.LoanHeaderID, T.LoanTicketNumber, T.UserID_FK, 
               U.UserName, U.Email, U.Phone, 
               T.TotalQty, T.LoanDt, T.LoanReturnDt, 
               T.CreatedBy, T.CreatedDt, T.UpdateBy, T.UpdateDt, T.Status
        FROM TransactionLoanHeaders T
        JOIN Users U ON T.UserID_FK = U.UserID
        WHERE T.IsDelete = 0 AND {column} LIKE ?
        ORDER BY T.LoanHeaderID DESC
        '''
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (f"%{keyword}%",))
        rows = cursor.fetchall()

        return [TransactionLoanHeaderDTO.from_row(row) for row in rows]

    def create_transaction_loan_header(self, request_dto: TransactionLoanHeaderRequestDTO,conn=None) -> int:
        try:
            if conn is None:
                conn = get_connection()
            now = localtime()
            loan_ticket_number = f"LMS-{datetime.datetime.now().strftime('%d%m%y-%H:%M:%S')}"
            query = '''
            INSERT INTO TransactionLoanHeaders 
            (LoanTicketNumber, UserID_FK, TotalQty, LoanDt, LoanReturnDt, IsDelete, CreatedBy, CreatedDt, UpdateBy, UpdateDt, Status) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            query_get_id = "SELECT @@IDENTITY AS ID;"
            cursor = conn.cursor()
            cursor.execute(query, (
                loan_ticket_number,
                request_dto.user_id,
                request_dto.total_qty,
                strftime("%Y-%m-%d %H:%M:%S", now),
                request_dto.loan_return_dt,
                0,
                ADMIN,
                strftime("%Y-%m-%d %H:%M:%S", now),
                ADMIN,
                strftime("%Y-%m-%d %H:%M:%S", now),
                0
            ))
            
            cursor.execute(query_get_id)
            header_id = cursor.fetchone()[0] 
            return header_id
        except Exception as e:
            print(f"Error create_transaction_loan_header: {e}")
            raise

    def update_status_revoke(self, loan_header_id: int, conn=None) -> None:
        if conn is None:
            conn = get_connection()
        query = "UPDATE TransactionLoanHeaders SET Status = 1 WHERE LoanHeaderID = ?"
        cursor = conn.cursor()
        cursor.execute(query, (loan_header_id,))

    def find_trans_header_loan(self, loan_header_id: int) -> Optional[TransactionLoanHeaderDTO]:
        query = f'''
        SELECT T.LoanHeaderID, T.LoanTicketNumber, T.UserID_FK, 
               U.UserName, U.Email, U.Phone, 
               T.TotalQty, T.LoanDt, T.LoanReturnDt, 
               T.CreatedBy, T.CreatedDt, T.UpdateBy, T.UpdateDt, T.Status
        FROM TransactionLoanHeaders T
        JOIN Users U ON T.UserID_FK = U.UserID
        WHERE T.IsDelete = 0 AND T.LoanHeaderID = ?
        '''
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (loan_header_id))
        row = cursor.fetchone()
        if row:
            return TransactionLoanHeaderDTO.from_row(row)
        return None
