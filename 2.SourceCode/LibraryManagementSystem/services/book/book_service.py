from typing import List
from domain.dto.book.book_transaction_loan_dto import BookTransactionLoanDTO
from domain.entities.genre_category import GenreCategory
from repositories.book.i_book_repository import IBookRepository
from repositories.category.i_category_repository import ICategoryRepository
from domain.dto.category.category_dto import GenreCategoryDTO
from domain.entities.book import Book

class BookService:
    _instance = None

    def __init__(self, book_repository: IBookRepository, category_repository: ICategoryRepository):
        self.book_repository = book_repository
        self.category_repository = category_repository

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            from repositories.book.book_repository import BookRepository
            from repositories.category.category_repository import CategoryRepository
            cls._instance = cls(
                book_repository=BookRepository(),
                category_repository=CategoryRepository()
            )
        return cls._instance

    def get_all_book_trans(self) -> List[BookTransactionLoanDTO]:
        books: List[Book] = self.book_repository.get_all_books()
        categories: List[GenreCategory] = self.category_repository.get_all_genre_categories()
        result: List[BookTransactionLoanDTO] = []

        for book in books:
            dto = BookTransactionLoanDTO(
                book_id=book.book_id,
                title=book.title,
                author=book.author,
                cover=book.cover,
                landing_page=book.landing_page,
                hashtag=book.hashtag,
                genre_category=book.genre_category,
                publisher=book.publisher,
                publish_year=book.publish_year,
                location=book.location,
                is_display=book.is_display,
                qty_oh=book.qty_oh,
                qty_allocated=book.qty_allocated,
                is_delete=book.is_deleted,
                created_dt=book.created_dt,
                created_by=book.created_by,
                update_dt=book.update_dt,
                update_by=book.update_by,
                is_out_of_stock=(book.qty_oh - book.qty_allocated) == 0
            )

            if dto.genre_category:
                genre_ids = [s.strip() for s in dto.genre_category.split(',')]
                genre_names = []
                for gid in genre_ids:
                    try:
                        gid_int = int(gid)
                        for cat in categories:
                            if cat.genre_category_id == gid_int:
                                genre_names.append(cat.name_category)
                                break
                    except ValueError:
                        continue
                dto.genre_category = ", ".join(genre_names)

            result.append(dto)

        return result