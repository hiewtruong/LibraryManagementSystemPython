from typing import List
from db_utils import get_connection, close
from domain.entities.author import Author
from repositories.author.i_author_repository import IAuthorRepository

class AuthorRepository(IAuthorRepository):
    _instance = None

    @staticmethod
    def get_instance():
        if AuthorRepository._instance is None:
            AuthorRepository._instance = AuthorRepository()
        return AuthorRepository._instance

    def get_all_authors(self) -> List[Author]:
        authors = []
        sql = """
            SELECT * FROM Authors
            WHERE IsDelete = 0
            ORDER BY AuthorID DESC
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                author = Author.from_row(row)
                authors.append(author)
        except Exception as e:
            print(f"Error fetching authors: {e}")
        finally:
            close()
        return authors