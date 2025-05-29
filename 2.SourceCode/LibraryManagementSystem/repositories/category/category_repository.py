from typing import List
from domain.entities.genre_category import GenreCategory
from db_utils import get_connection, close
from repositories.category.i_category_repository import ICategoryRepository

class CategoryRepository(ICategoryRepository):
    def get_all_genre_categories(self) -> List[GenreCategory]:
        genre_categories = []
        query = """
            SELECT GenreCategoryID, NameCategory, GenreCategory, IsDelete, 
                   CreatedDt, CreatedBy, UpdateDt, UpdateBy
            FROM GenreCategories
            WHERE IsDelete = 0
            ORDER BY GenreCategoryID DESC
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                genre_category = GenreCategory(
                    genre_category_id=row[0],
                    name_category=row[1],
                    genre_category=row[2],
                    is_delete=row[3],
                    created_dt=row[4],
                    created_by=row[5],
                    update_dt=row[6],
                    update_by=row[7]
                )
                genre_categories.append(genre_category)

        except Exception as e:
            print(f"[GenreCategoryService.get_all_genre_categories] Error: {e}")
            raise
        finally:
            close()

        return genre_categories
