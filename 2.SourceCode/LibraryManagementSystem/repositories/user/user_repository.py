from typing import List
from db_utils import get_connection, close
from domain.dto.user.user_login_dto import UserLoginDTO
from domain.dto.user.user_role_dto import UserRoleDTO
from repositories.user.i_user_repository import IUserRepository

class UserRepository(IUserRepository):
    def get_user_by_username(self, username):
        query = '''
            SELECT u.UserName, u.Password, ur.UserRoleID, ur.RoleName 
            FROM Users u 
            JOIN UserRoles ur ON u.UserRoleID_FK = ur.UserRoleID 
            WHERE u.UserName = ?
        '''
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (username,))
            result = cursor.fetchone()

            if result:
                return UserLoginDTO(
                    user_name=result[0],
                    password=result[1],
                    user_role_id=result[2],
                    role_name=result[3]
                )
            return None
        except Exception as e:
            print(f"[UserRepository] Lỗi khi truy vấn: {e}")
            raise
        finally:
            close()
    
    def get_all_users_customer(self) -> List[UserRoleDTO]:
        user_list = []
        sql = """
            SELECT u.*, r.RoleName, r.IsAdmin
            FROM Users u
            JOIN UserRoles r ON u.UserRoleID_FK = r.UserRoleID
            WHERE u.IsDelete = 0 AND r.IsAdmin = 0
            ORDER BY u.UserID DESC
        """
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                user = UserRoleDTO(*row)
                user_list.append(user)
        except Exception as e:
            raise RuntimeError(f"Error retrieving users: {str(e)}")
        finally:
            close()
        return user_list

    def get_all_users_customer_by_search(self, keyword: str, column: str) -> List[UserRoleDTO]:
        user_list = []
        sql_template = """
            SELECT u.*, r.RoleName, r.IsAdmin
            FROM Users u
            JOIN UserRoles r ON u.UserRoleID_FK = r.UserRoleID
            WHERE u.IsDelete = 0 AND r.IsAdmin = 0
            AND {} LIKE ?
            ORDER BY u.UserID DESC
        """
        sql = sql_template.format(column)
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (f"%{keyword}%",))
            rows = cursor.fetchall()
            for row in rows:
                user = UserRoleDTO(*row)
                user_list.append(user)
        except Exception as e:
            raise RuntimeError(f"Error retrieving users by search: {str(e)}")
        finally:
            close()
        return user_list
