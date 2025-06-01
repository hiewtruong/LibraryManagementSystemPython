from abc import ABC, abstractmethod
from typing import List
from domain.dto.user.user_dto import UserDTO
from domain.dto.user.user_login_dto import UserLoginDTO

class IUserService(ABC):
    @abstractmethod
    def get_user_by_username(self, username: str, password_input: str, parent=None) -> UserLoginDTO:
        pass

    @abstractmethod
    def get_all_users_customer(self) -> List[UserDTO]:
        pass
