from typing import List
from db_utils import get_connection, close
from domain.dto.user.user_login_dto import UserLoginDTO
from domain.dto.user.user_role_dto import UserRoleDTO
from domain.dto.user.user_dto import UserDTO
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
            print(f"[UserRepository] Error querying user by username: {e}")
            raise
        finally:
            close()

    def get_all_user_roles(self) -> list:
        query = '''
            SELECT UserRoleID, RoleName, IsAdmin, IsDelete
            FROM UserRoles
            WHERE IsDelete = 0
        '''
        conn = None
        roles = []
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                role = UserRoleDTO(
                    user_role_id_fk=row[0],
                    role_name=row[1],
                    is_admin=row[2],
                    is_delete=row[3]
                )
                roles.append(role)
            return roles
        except Exception as e:
            print(f"[UserRepository] Error retrieving user roles: {e}")
            raise
        finally:
            close()
    
    def get_all_users_customer(self) -> List[UserRoleDTO]:
        user_list = []
        sql = """
                SELECT 
                u.UserID,
                u.FirstName,
                u.LastName,
                u.UserName,
                u.Password,
                u.Gender,
                u.Email,
                u.Phone,
                u.Address,
                u.UserRoleID_FK,
                u.IsDelete,
                r.RoleName,
                r.IsAdmin
            FROM Users u
            JOIN UserRoles r ON u.UserRoleID_FK = r.UserRoleID
            ORDER BY u.UserID DESC
        """
        conn = None
        try:
            conn = get_connection()
            if conn is None:
                raise RuntimeError("Database connection failed.")
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                user = UserRoleDTO.from_row(row)
                user_list.append(user)
        except Exception as e:
            raise RuntimeError(f"Error retrieving users: {str(e)}")
        finally:
            close()
        return user_list

    def get_all_users_customer_by_search(self, keyword: str, column: str) -> List[UserRoleDTO]:
        user_list = []
        sql_template = """
            SELECT 
                u.UserID,
                u.FirstName,
                u.LastName,
                u.UserName,
                u.Password,
                u.Gender,
                u.Email,
                u.Phone,
                u.Address,
                u.UserRoleID_FK,
                u.IsDelete,
                r.RoleName,
                r.IsAdmin
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
                user = UserRoleDTO.from_row(row)
                user_list.append(user)
        except Exception as e:
            raise RuntimeError(f"Error retrieving users by search: {str(e)}")
        finally:
            close()
        return user_list

    def is_email_duplicate(self, email: str) -> bool:
        query = '''
            SELECT 1 FROM Users WHERE Email = ? AND IsDelete = 0
        '''
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            return result is not None
        except Exception as e:
            print(f"[UserRepository] Error checking duplicate email: {e}")
            raise
        finally:
            close()

    def create_user(self, user_dto: UserDTO) -> bool:
        query = '''
            INSERT INTO Users (UserName, Email, FirstName, LastName, Gender, Phone, Address, UserRoleID_FK, IsDelete, CreatedDT, CreatedBy, UpdateDT, UpdateBy)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (
                user_dto.user_name,
                user_dto.email,
                user_dto.first_name,
                user_dto.last_name,
                user_dto.gender,
                user_dto.phone,
                user_dto.address,
                user_dto.user_role_id,
                user_dto.is_delete,
                user_dto.created_dt,
                user_dto.created_by,
                user_dto.update_dt,
                user_dto.update_by
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"[UserRepository] Error creating user: {e}")
            raise
        finally:
            close()

    def update_user(self, user_dto: UserDTO) -> bool:
        query = '''
            UPDATE Users
            SET FirstName = ?, LastName = ?, UserName = ?, Password = ?, Gender = ?, Email = ?, Phone = ?, Address = ?, UserRoleID_FK = ?, IsDelete = ?, UpdateDT = ?, UpdateBy = ?
            WHERE UserID = ?
        '''
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (
                user_dto.first_name,
                user_dto.last_name,
                user_dto.user_name,
                user_dto.password,
                user_dto.gender,
                user_dto.email,
                user_dto.phone,
                user_dto.address,
                user_dto.user_role_id,
                user_dto.is_delete,
                user_dto.update_dt,
                user_dto.update_by,
                user_dto.user_id
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"[UserRepository] Error updating user: {e}")
            raise
        finally:
            close()

    def delete_user(self, user_id: int) -> bool:
        query = '''
            DELETE FROM Users
            WHERE UserID = ?
        '''
        conn = None
        try:
            conn = get_connection()
            if conn is None:
                print("[UserRepository] Database connection failed in delete_user.")
                return False
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            conn.commit()
            print(f"[UserRepository] User with ID {user_id} deleted from database.")
            return True
        except Exception as e:
            print(f"[UserRepository] Error deleting user: {e}")
            return False
        finally:
            close()
