from typing import List
from domain.dto.user.user_dto import UserDTO
from domain.dto.user.user_role_dto import UserRoleDTO
from lib.notifier_utils import show_error
from lib.crypto_utils import encrypt_password
from lib.constants import NOT_FOUND_USER, ROLE_ADMIN, WRONG_PASSWORD
from repositories.user.i_user_repository import IUserRepository
from repositories.user.user_repository import UserRepository
from services.user.i_user_service import IUserService
from domain.dto.user.user_login_dto import UserLoginDTO

class UserService(IUserService):
    _instance = None

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    @classmethod
    def get_instance(cls, user_repository: IUserRepository = None):
        if cls._instance is None:
            cls._instance = cls(user_repository=user_repository)
        return cls._instance

    def get_user_by_username(self, username: str, password_input: str, parent=None) -> UserLoginDTO or None:
        try:
            user_dto = self.user_repository.get_user_by_username(username)

            if not user_dto:
                show_error(parent, NOT_FOUND_USER.format(username))
                return None

            if not self._compare_password(user_dto.password, password_input, parent):
                return None

            if user_dto.user_role_id != ROLE_ADMIN:
                show_error(parent, NOT_FOUND_USER.format(username))
                return None

            return user_dto

        except Exception as e:
            raise Exception(f"[UserService.get_user_by_username] Exception: {str(e)}")

    def _compare_password(self, password_db: str, password_input: str, parent=None) -> bool:
        encrypted_input = encrypt_password(password_input)
        if password_db != encrypted_input:
            show_error(parent, WRONG_PASSWORD)
            return False
        return True
    
    def get_all_users_customer(self) -> List[UserRoleDTO]:
        if not self.user_repository:
            self.user_repository = UserRepository()
        users = self.user_repository.get_all_users_customer()
        return users

    def is_email_duplicate(self, email: str) -> bool:
        if not self.user_repository:
            self.user_repository = UserRepository()
        return self.user_repository.is_email_duplicate(email)

    def create_user(self, user_dto: UserDTO) -> bool:
        if self.is_email_duplicate(user_dto.email):
            raise Exception("Email already exists.")
        # Encrypt password before saving
        if user_dto.password:
            user_dto.password = encrypt_password(user_dto.password)
        return self.user_repository.create_user(user_dto)

    def update_user(self, user_dto: UserDTO) -> bool:
        try:
            # Encrypt password if changed before updating
            if user_dto.password:
                user_dto.password = encrypt_password(user_dto.password)
            return self.user_repository.update_user(user_dto)
        except Exception as e:
            raise Exception(f"[UserService.update_user] Exception: {str(e)}")

    def delete_user(self, user_id: int) -> bool:
        try:
            return self.user_repository.delete_user(user_id)
        except Exception as e:
            print(f"[UserService.delete_user] Exception: {str(e)}")
            return False

    def get_all_user_roles(self) -> List[UserRoleDTO]:
        if not self.user_repository:
            self.user_repository = UserRepository()
        return self.user_repository.get_all_user_roles()

    def get_all_users(self) -> List[UserDTO]:
        if not self.user_repository:
            self.user_repository = UserRepository()
        user_role_dtos = self.user_repository.get_all_users_customer()
        user_dtos = []
        for ur in user_role_dtos:
            user_dto = UserDTO(
                user_id=ur.user_id,
                first_name=ur.first_name,
                last_name=ur.last_name,
                user_name=ur.user_name,
                password=ur.password,
                email=ur.email,
                phone=ur.phone,
                address=ur.address,
                gender=ur.gender,
                user_role_id=ur.user_role_id_fk,
                is_delete=ur.is_delete,
                is_admin=ur.is_admin,
                role_name=ur.role_name,
                created_dt=None,
                created_by=None,
                update_dt=None,
                update_by=None
            )
            user_dtos.append(user_dto)
        return user_dtos

