from domain.dto.user_login_dto import UserLoginDTO
from repositories.user_repository import UserRepository
from lib.crypto_utils import encrypt_password
from tkinter import messagebox
from lib.constants import NOT_FOUND_USER,ERROR, ROLE_ADMIN,WRONG_PASSWORD

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def get_user_by_username(self, username, passwordInput):
        try:
            user_dto = self.user_repository.get_user_by_username(username)
            if user_dto:
                isSuccess = self.comparePassword(user_dto.password,passwordInput)
                if isSuccess == False:
                    return None
                else:
                    if user_dto.user_role_id != ROLE_ADMIN:
                        messagebox.showerror(ERROR,NOT_FOUND_USER.format(username))
                        return None
                    else:
                        return user_dto
            else:
                messagebox.showerror(ERROR,NOT_FOUND_USER.format(username))
                return None
        except Exception as e:
            raise Exception(f"Lỗi khi lấy thông tin người dùng: {str(e)}")
    
    def comparePassword(self, passwordDb : str, passwordInput: str):
        encryptPass = encrypt_password(passwordInput);
        if passwordDb != encryptPass:
            messagebox.showerror(ERROR,"Mật khẩu nhập vào không chính xác, vui lòng nhập lại")
            return False
        else:
            return True