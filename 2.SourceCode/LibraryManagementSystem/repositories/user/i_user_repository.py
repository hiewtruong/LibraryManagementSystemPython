from abc import ABC, abstractmethod
from typing import List
from domain.dto.user.user_login_dto import UserLoginDTO
from domain.dto.user.user_role_dto import UserRoleDTO

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
