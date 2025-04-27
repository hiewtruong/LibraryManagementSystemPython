import tkinter as tk
from tkinter import messagebox
from controllers.user_controller import UserController
from lib.constants import MISSING_USER_OR_PASSWORD, ERROR
import os
from PIL import Image, ImageTk

class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management - Admin Login")
        self._center_window(900, 400)
        self.root.resizable(False, False)
        self.controller = UserController()
        self._build_ui()

    def _center_window(self, width, height):
        """Căn giữa cửa sổ"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _build_ui(self):
        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(fill="both", expand=True)

        # --- Left Frame (Ảnh nền) ---
        left_frame = tk.Frame(main_frame, width=500)
        left_frame.pack(side="left", fill="both", expand=False)

        image_path = os.path.join("resources", "img", "login_img.jpg")  # Thay đường dẫn ảnh nếu cần
        if os.path.exists(image_path):
            image = Image.open(image_path)
            bg_image = ImageTk.PhotoImage(image)
            bg_label = tk.Label(left_frame, image=bg_image)
            bg_label.place(relwidth=1, relheight=1)
            bg_label.image = bg_image  # Giữ tham chiếu ảnh
        else:
            # Nếu không có ảnh, hiện thông báo
            tk.Label(left_frame, text="Không tìm thấy ảnh", bg="gray", fg="white").pack(expand=True)

        # --- Right Frame (Form Login) ---
        right_frame = tk.Frame(main_frame, bg="white", padx=20, pady=20)
        right_frame.pack(side="right", fill="both", expand=True)

        title_label = tk.Label(
            right_frame,
            text="Welcome to Library Management System",
            font=("Helvetica", 16, "bold"),
            fg="#333",
            bg="white"
        )
        title_label.pack(pady=(20, 30))

        # Username
        tk.Label(right_frame, text="Tài khoản:", bg="white", anchor="w").pack(fill="x")
        self.username_entry = tk.Entry(right_frame, width=40, bg="white", highlightthickness=0, highlightbackground="black")
        self.username_entry.pack(pady=(5, 15))

        # Password
        tk.Label(right_frame, text="Mật khẩu:", bg="white", anchor="w").pack(fill="x")
        self.password_entry = tk.Entry(right_frame, show="*", width=40, bg="white", highlightthickness=0, highlightbackground="black")
        self.password_entry.pack(pady=(5, 20))

        # Login Button
        login_button = tk.Button(
            right_frame,
            text="Đăng nhập",
            width=20,
            command=self.handle_login,
            bg="white",
            fg="black",
            activebackground="white",
            relief="flat",
            highlightthickness=1,
            highlightbackground="white"
        )
        login_button.pack(pady=5)

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning(ERROR, MISSING_USER_OR_PASSWORD)
            return
        try:
            self.controller.get_user_by_username(self.root, username, password)
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Không thể đăng nhập: {str(e)}")