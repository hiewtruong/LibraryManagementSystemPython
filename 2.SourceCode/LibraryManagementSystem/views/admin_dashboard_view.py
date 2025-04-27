import tkinter as tk
from tkinter import ttk

from views.book.book_panel import BookPanel
from views.author.author_panel import AuthorPanel
from views.category.category_panel import CategoryPanel
from views.transactions_loan.create_transaction_loan_panel import CreateTransactionLoanPanel
from views.transactions_loan.transaction_loan_panel import TransactionLoanPanel
from lib.common_ui.confirm_modal import ConfirmModal  

class AdminDashboardFrame(tk.Tk):
    def __init__(self, user_dto):
        super().__init__()
        self.title("Admin Dashboard")
        self.geometry("1600x900")
        self.configure(bg="white")
        self.user_dto = user_dto

        self.current_panel = None 

        self._center_window(1600, 900)
        self.resizable(False, False)

        self._init_ui()

    def _center_window(self, width, height):
        """Căn giữa cửa sổ."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _init_ui(self):
        menu_wrapper = tk.Frame(self, width=240, height=900, bg="white", padx=10, pady=20)
        menu_wrapper.pack(side="left", fill="y")
        menu_wrapper.pack_propagate(False)

        tk.Label(menu_wrapper, text="Menu", font=("Arial", 24, "bold"), bg="white").pack(expand=False, fill="x", pady=(0, 14))

        menu_frame = tk.Frame(menu_wrapper, bg="white", highlightbackground="gray", highlightthickness=1)
        menu_frame.pack(fill="x", pady=(0, 20))

        book_btn = tk.Button(menu_frame, text="Quản lý Sách", command=self.show_book_panel, width=20, highlightbackground="white")
        author_btn = tk.Button(menu_frame, text="Quản lý Tác giả", command=self.show_author_panel, width=20, highlightbackground="white")
        genre_btn = tk.Button(menu_frame, text="Quản lý Thể loại", command=self.show_category_panel, width=20, highlightbackground="white")
        transaction_loan_btn = tk.Button(menu_frame, text="Quản lý Thuê/mượn sách", command=self.show_transaction_loan_panel, width=20, highlightbackground="white")
        create_transaction_loan_btn = tk.Button(menu_frame, text="Tạo đơn thuê/mượn sách", command=self.show_create_transaction_loan_panel, width=20, highlightbackground="white")

        for btn in [book_btn, author_btn, genre_btn, transaction_loan_btn, create_transaction_loan_btn]:
            btn.pack(pady=10, padx=10)

        exit_wrapper = tk.Frame(menu_wrapper, bg="white")
        exit_wrapper.pack(side="bottom", fill="x")
        
        exit_btn = tk.Button(exit_wrapper, text="Thoát", command=self._confirm_exit, bg="white", fg="red", highlightbackground="white")
        exit_btn.pack(side="bottom", fill="x", padx=10, pady=1)

        content_wrapper = tk.Frame(self, height=900, bg="white", padx=20, pady=18)
        content_wrapper.pack(side="right", expand=True, fill="both")
        content_wrapper.pack_propagate(False) 

        top_right_panel = tk.Frame(content_wrapper, bg="white")
        top_right_panel.pack(side="top", anchor="ne", pady=(0, 10), padx=(10, 10))

        user_label = tk.Label(top_right_panel, text=f"{self.user_dto.user_name}", font=("Arial", 12, "italic"), fg="gray", bg="white")
        role_label = tk.Label(top_right_panel, text=f"Role: {self.user_dto.role_name}", font=("Arial", 12), bg="white")
        user_label.pack(anchor="e")
        role_label.pack(anchor="e")

        content_frame = tk.Frame(content_wrapper, bg="white", highlightbackground="gray", highlightthickness=1)
        content_frame.pack(expand=True, fill="both")

        self.content_panel = tk.Frame(content_frame, bg="white")
        self.content_panel.pack(expand=True, fill="both")

        self.welcome_label = tk.Label(
            self.content_panel,
            text="Xin chào mừng đến với hệ thống quản lý sách LMS",
            font=("Arial", 24, "bold"),
            bg="white"
        )
        self.welcome_label.pack(expand=True)

    def clear_content(self):
        if self.current_panel is not None:
            self.current_panel.destroy() 
            self.current_panel = None

        for widget in self.content_panel.winfo_children():
            widget.destroy()

    def show_book_panel(self):
        self.clear_content()
        self.current_panel = BookPanel(self.content_panel)
        self.current_panel.pack(expand=True, fill="both")

    def show_author_panel(self):
        self.clear_content()
        self.current_panel = AuthorPanel(self.content_panel)
        self.current_panel.pack(expand=True, fill="both")

    def show_category_panel(self):
        self.clear_content()
        self.current_panel = CategoryPanel(self.content_panel)
        self.current_panel.pack(expand=True, fill="both")
        
    def show_transaction_loan_panel(self):
        self.clear_content()
        self.current_panel = TransactionLoanPanel(self.content_panel)
        self.current_panel.pack(expand=True, fill="both")
        
    def show_create_transaction_loan_panel(self):
        self.clear_content()
        self.current_panel = CreateTransactionLoanPanel(self.content_panel)
        self.current_panel.pack(expand=True, fill="both")

    def _confirm_exit(self):
        modal = ConfirmModal(self, message="Bạn có chắc chắn muốn thoát không?", title="Xác nhận thoát")
        result = modal.get_result()
        if result:
            self.destroy()