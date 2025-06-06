from abc import ABC, abstractmethod
from typing import List
from domain.dto.user.user_login_dto import UserLoginDTO
from domain.dto.user.user_role_dto import UserRoleDTO
from domain.dto.user.user_dto import UserDTO

class IUserRepository(ABC):
    @abstractmethod
    def get_user_by_username(self, username: str) -> UserLoginDTO:
        pass

    @abstractmethod
    def get_all_users_customer(self) -> List[UserRoleDTO]:
        pass

    @abstractmethod
    def get_all_users_customer_by_search(self, keyword: str, column: str) -> List[UserRoleDTO]:
        pass

    @abstractmethod
    def is_email_duplicate(self, email: str) -> bool:
        pass

    @abstractmethod
    def create_user(self, user_dto: UserDTO) -> bool:
        pass

    @abstractmethod
    def update_user(self, user_dto: UserDTO) -> bool:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def get_all_user_roles(self) -> List[UserRoleDTO]:
        pass
