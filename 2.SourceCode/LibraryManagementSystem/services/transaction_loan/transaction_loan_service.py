from datetime import datetime
from typing import List
from lib.constants import LOAN_BOOK_SUBJECT, TRANS_BORROW, TRANS_PAID
from repositories.transaction_loan.i_transaction_loan_header_repository import ITransactionLoanHeaderRepository
from repositories.transaction_loan.i_transaction_loan_detail_repository import ITransactionLoanDetailRepository
from repositories.book.i_book_repository import IBookRepository
from repositories.user.i_user_repository import IUserRepository
from repositories.category.i_category_repository import ICategoryRepository
from domain.dto.transaction.transaction_loan_header_dto import TransactionLoanHeaderDTO
from domain.dto.transaction.transaction_loan_detail_dto import TransactionLoanDetailDTO
from domain.dto.transaction.transaction_loan_header_request_dto import TransactionLoanHeaderRequestDTO
from domain.dto.transaction.transaction_loan_header_revoke_dto import TransactionLoanHeaderRevokeDTO
from domain.dto.transaction.transaction_send_email_dto import TransactionSendEmailDTO
from domain.dto.book.book_send_email_dto import BookSendEmail
from domain.entities.transaction_loan_header import TransactionLoanHeader
from db_utils.database_core import DbUtils 
from lib.email_utils import send_email, generate_loan_email_content


class TransactionLoanService:
    _instance = None

    def __init__(
        self,
        header_repo: ITransactionLoanHeaderRepository,
        detail_repo: ITransactionLoanDetailRepository,
        book_repo: IBookRepository,
        user_repo: IUserRepository,
        category_repo: ICategoryRepository
    ):
        self.header_repo = header_repo
        self.detail_repo = detail_repo
        self.book_repo = book_repo
        self.user_repo = user_repo
        self.category_repo = category_repo

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            from repositories.transaction_loan.transaction_loan_header_repository import TransactionLoanHeaderRepository
            from repositories.transaction_loan.transaction_loan_detail_repository import TransactionLoanDetailRepository
            from repositories.book.book_repository import BookRepository
            from repositories.user.user_repository import UserRepository
            from repositories.category.category_repository import CategoryRepository

            cls._instance = cls(
                header_repo=TransactionLoanHeaderRepository(),
                detail_repo=TransactionLoanDetailRepository(),
                book_repo=BookRepository(),
                user_repo=UserRepository(),
                category_repo=CategoryRepository()
            )
        return cls._instance

    def get_all_transaction_headers(self, keyword: str = "", column: str = "") -> List[TransactionLoanHeaderDTO]:
        if keyword:
            headers = self.header_repo.get_all_trans_headers_by_keyword(keyword, column)
        else:
            headers = self.header_repo.get_all_trans_headers()
        now = datetime.now().date()
        for h in headers:
            if h.status == TRANS_BORROW:
                h.set_status_name("BORROW")
            if h.status == TRANS_PAID:
                h.set_status_name("PAID")
            date_return =  h.loan_return_dt.date()
            if now > date_return and h.status == TRANS_BORROW:
                h.set_expired(1)
        return headers

    def get_transaction_details(self, header_id: int) -> List[TransactionLoanDetailDTO]:
        categories = self.category_repo.get_all_genre_categories()
        details = self.detail_repo.get_transaction_loans_by_header_id(header_id)

        for detail in details:
            genre_ids = detail.genre_category.split(",") if detail.genre_category else []
            genre_names = [
                cat.get_name_category() for gid in genre_ids
                if (cat := next((c for c in categories if c.genre_category_id == int(gid)), None))
            ]
            detail.genre_category = ", ".join(genre_names)
        return details

    def create_transaction(self, request: TransactionLoanHeaderRequestDTO):
        try:
            with DbUtils.transaction() as conn:
                header_id = self.header_repo.create_transaction_loan_header(request,conn)
                self.detail_repo.create_transaction_loan_details(header_id, request.loan_details,conn)
                self.book_repo.update_qty_allocated(request.loan_details,conn)
            send_data = self._prepare_email_data(header_id, request.loan_details)
            email_body = generate_loan_email_content(send_data)
            subject = LOAN_BOOK_SUBJECT.format(send_data.loan_ticket_number)
            send_email(send_data.email, subject, email_body)
        except Exception as e:
            raise
        finally:
            pass

    def revoke_transaction(self, request: TransactionLoanHeaderRevokeDTO):
        try:
            with DbUtils.transaction() as conn:
                self.header_repo.update_status_revoke(request.loan_header_id, conn=conn)
                self.book_repo.decrement_qty_allocated(request.loan_details,conn=conn)
        except Exception as e:
            raise
        finally:
            pass

    def _prepare_email_data(self, header_id: int, details: List) -> TransactionSendEmailDTO:
        header: TransactionLoanHeader = self.header_repo.find_trans_header_loan(header_id)
        users = self.user_repo.get_all_users_customer()
        books = self.book_repo.get_all_books()

        send_data = TransactionSendEmailDTO(
            loan_ticket_number=header.loan_ticket_number,
            total_qty=header.total_qty,
            loan_dt=header.loan_dt,
            loan_return_dt=header.loan_return_dt,
        )

        user = next((u for u in users if u.user_id == header.user_id), None)
        if user:
            send_data.use_name = user.user_name
            send_data.phone = user.phone
            send_data.email = user.email

        book_map = {book.book_id: book for book in books}
        book_details = [
            BookSendEmail(
                book_id=book.book_id,
                title=book.title,
                author=book.author
            )
            for d in details if (book := book_map.get(d.load_book_id))
        ]
        send_data.book_details = book_details
        return send_data
