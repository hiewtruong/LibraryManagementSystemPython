from typing import List
from domain.entities.genre_category import GenreCategory
from db_utils import get_connection, close
from repositories.category.i_category_repository import ICategoryRepository

class CategoryRepository(ICategoryRepository):
    def get_all_genre_categories(self) -> List[GenreCategory]:
        genre_categories = []
        query = """
            SELECT GenreCategoryID, NameCategory, GenreCategory, 
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
                    created_dt=row[3],
                    created_by=row[4],
                    update_dt=row[5],
                    update_by=row[6]
                )
                genre_categories.append(genre_category)

        except Exception as e:
            print(f"[GenreCategoryService.get_all_genre_categories] Error: {e}")
            raise
        finally:
            close()

        return genre_categories

    def get_in_ids(self, ids: str) -> List[GenreCategory]:
        genre_categories = []
        if not ids:
            return genre_categories

        query = f"""
            SELECT GenreCategoryID, NameCategory, GenreCategory, 
                CreatedDt, CreatedBy, UpdateDt, UpdateBy
            FROM GenreCategories
            WHERE IsDelete = 0 AND GenreCategoryID IN ({ids})
            ORDER BY GenreCategoryID DESC
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                genre_category = GenreCategory.from_row(row)
                genre_categories.append(genre_category)

        except Exception as e:
            print(f"[GenreCategoryService.get_in_ids] Error: {e}")
            raise
        finally:
            close()

        return genre_categories

    def find_all(self) -> List[GenreCategory]:
        genre_categories = []
        query = """
            SELECT GenreCategoryID, NameCategory, GenreCategory, 
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
                genre_category = GenreCategory.from_row(row)
                genre_categories.append(genre_category)

        except Exception as e:
            print(f"[GenreCategoryService.find_all] Error: {e}")
            raise
        finally:
            close()

        return genre_categories

    def add_category(self, category: GenreCategory) -> GenreCategory:
        query = """
            INSERT INTO GenreCategories (NameCategory, GenreCategory, 
                CreatedDt, CreatedBy, UpdateDt, UpdateBy, IsDelete)
            VALUES (?, ?, CURRENT_TIMESTAMP, ?, CURRENT_TIMESTAMP, ?, 0)
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (
                category.name_category,
                category.genre_category,
                category.created_by,
                category.update_by
            ))
            conn.commit()
            cursor.execute("SELECT SCOPE_IDENTITY()")
            category_id = cursor.fetchone()[0]
            category.set_genre_category_id(category_id)
        except Exception as e:
            print(f"[GenreCategoryService.add_category] Error: {e}")
            raise
        finally:
            close()

        return category
    
    def update_category(self, category: GenreCategory) -> GenreCategory:
        query = """
            UPDATE GenreCategories
            SET NameCategory = ?, GenreCategory = ?, 
                UpdateDt = CURRENT_TIMESTAMP, UpdateBy = ?
            WHERE GenreCategoryID = ?
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (
                category.name_category,
                category.genre_category,
                category.update_by,
                category.genre_category_id
            ))
            conn.commit()
        except Exception as e:
            print(f"[GenreCategoryService.update_category] Error: {e}")
            raise
        finally:
            close()

        return category
    
    def delete_category(self, genre_category_id: int) -> bool:
        query = """
            UPDATE GenreCategories
            SET IsDelete = 1, UpdateDt = CURRENT_TIMESTAMP, UpdateBy = 'admin'
            WHERE GenreCategoryID = ?
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (genre_category_id,))
            conn.commit()
            if cursor.rowcount == 0:
                return False
        except Exception as e:
            print(f"[GenreCategoryService.delete_category] Error: {e}")
            raise
        finally:
            close()
        return True
    
    def get_category_by_id(self, genre_category_id: int) -> GenreCategory:
        query = """
            SELECT GenreCategoryID, NameCategory, GenreCategory, 
                CreatedDt, CreatedBy, UpdateDt, UpdateBy
            FROM GenreCategories
            WHERE GenreCategoryID = ? AND IsDelete = 0
        """
        genre_category = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (genre_category_id,))
            row = cursor.fetchone()
            if row:
                genre_category = GenreCategory.from_row(row)
        except Exception as e:
            print(f"[GenreCategoryService.get_category_by_id] Error: {e}")
            raise
        finally:
            close()

        return genre_category