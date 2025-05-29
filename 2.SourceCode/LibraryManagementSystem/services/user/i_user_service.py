from abc import ABC, abstractmethod
from domain.dto.user.user_login_dto import UserLoginDTO

class IUserService(ABC):
    @abstractmethod
    def get_user_by_username(self, username: str, password_input: str, parent=None) -> UserLoginDTO:
        pass
