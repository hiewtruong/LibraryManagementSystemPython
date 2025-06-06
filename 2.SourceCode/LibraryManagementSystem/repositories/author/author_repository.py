from typing import List
from domain.entities.author import Author
from repositories.author.i_author_repository import IAuthorRepository
from db_utils import DbUtils
import pyodbc

class AuthorRepository(IAuthorRepository):

    def get_all_authors(self) -> List[Author]:
        authors = []
        sql = "SELECT * FROM [dbo].[Authors] WHERE IsDelete = 0 ORDER BY AuthorID desc"
        try:
            conn = DbUtils.get_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                author = Author()
                author.author_id = row.AuthorID
                author.author_name = row.AuthorName
                author.is_deleted = row.IsDelete
                author.created_dt = row.CreatedDt
                author.created_by = row.CreatedBy
                author.update_dt = row.UpdateDt
                author.update_by = row.UpdateBy
                authors.append(author)
            cursor.close()
        except pyodbc.Error as e:
            print(f"Database error: {e}")
        finally:
            DbUtils.close()
        return authors

    def get_authors_by_name(self, keyword: str) -> List[Author]:
        authors = []
        sql = "SELECT * FROM [dbo].[Authors] WHERE AuthorName LIKE ? AND IsDelete = 0 ORDER BY AuthorID desc"
        try:
            conn = DbUtils.get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, f"%{keyword}%")
            rows = cursor.fetchall()
            for row in rows:
                author = Author()
                author.author_id = row.AuthorID
                author.author_name = row.AuthorName
                author.is_deleted = row.IsDelete
                author.created_dt = row.CreatedDt
                author.created_by = row.CreatedBy
                author.update_dt = row.UpdateDt
                author.update_by = row.UpdateBy
                authors.append(author)
            cursor.close()
        except pyodbc.Error as e:
            print(f"Database error: {e}")
        finally:
            DbUtils.close()
        return authors

    def create_author(self, author: Author) -> bool:
        is_success = False
        sql = "INSERT INTO [dbo].[Authors] (AuthorName, IsDelete, CreatedDt, CreatedBy, UpdateDt, UpdateBy) VALUES (?, 0, GETDATE(), ?, GETDATE(), ?)"
        try:
            DbUtils.begin_transaction()
            conn = DbUtils.get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, author.author_name, author.created_by, author.created_by)
            if cursor.rowcount > 0:
                DbUtils.commit()
                is_success = True
            else:
                DbUtils.rollback()
            cursor.close()
        except pyodbc.Error as e:
            print(f"Database error: {e}")
            DbUtils.rollback()
        finally:
            DbUtils.close()
        return is_success

    def update_author(self, author: Author) -> bool:
        is_success = False
        sql = "UPDATE [dbo].[Authors] SET AuthorName = ?, IsDelete = ?, UpdateDt = GETDATE(), UpdateBy = ? WHERE AuthorID = ?"
        try:
            DbUtils.begin_transaction()
            conn = DbUtils.get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, author.author_name, author.is_deleted, author.update_by, author.author_id)
            if cursor.rowcount > 0:
                DbUtils.commit()
                is_success = True
            else:
                DbUtils.rollback()
            cursor.close()
        except pyodbc.Error as e:
            print(f"Database error: {e}")
            DbUtils.rollback()
        finally:
            DbUtils.close()
        return is_success

    def delete_author(self, author_id: int) -> bool:
        is_success = False
        sql = "UPDATE [dbo].[Authors] SET IsDelete = 1 WHERE AuthorID = ?"
        try:
            DbUtils.begin_transaction()
            conn = DbUtils.get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, author_id)
            if cursor.rowcount > 0:
                DbUtils.commit()
                is_success = True
            else:
                DbUtils.rollback()
            cursor.close()
        except pyodbc.Error as e:
            print(f"Database error: {e}")
            DbUtils.rollback()
        finally:
            DbUtils.close()
        return is_success
