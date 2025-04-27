from services.user_service import UserService
from views.admin_dashboard_view import AdminDashboardFrame
import tkinter as tk

class UserController:
    def __init__(self):
        self.user_service = UserService()

    def get_user_by_username(self,root,username, password):
        userDTO = self.user_service.get_user_by_username(username,password)
        if userDTO != None:
            root.destroy() 
            dashboard = AdminDashboardFrame(userDTO)
            dashboard.mainloop()

     