# repositories/user_repository.py
from db_utils.connection import DatabaseConnection
from domain.dto.user_login_dto import UserLoginDTO

class UserRepository:
    def __init__(self):
        self.db = DatabaseConnection()

    def get_user_by_username(self, username):
        query = '''
            SELECT u.UserName, u.Password, ur.UserRoleID, ur.RoleName 
            FROM Users u 
            JOIN UserRoles ur ON u.UserRoleID_FK = ur.UserRoleID 
            WHERE u.UserName = ?
        '''
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (username))
            result = cursor.fetchone()

            if result:
                user_dto = UserLoginDTO(
                    user_name=result[0],
                    password=result[1],
                    user_role_id=result[2],
                    role_name=result[3]
                )
                return user_dto
            return None
        except Exception as e:
            print(f"Lỗi khi truy vấn: {e}")
            raise
        finally:
            self.db.close()