import tkinter as tk
from tkinter import ttk

class ConfirmModal(tk.Toplevel):
    def __init__(self, parent, message="Are you sure?", title="Confirmation"):
        super().__init__(parent)
        self.parent = parent
        self.message = message
        self.title(title)
        self.result = None

        # Đặt màu nền của Toplevel thành trắng
        self.configure(bg="white")

        self.geometry("400x200")
        self._center_window(400, 200)
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self._init_ui()

    def _center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _init_ui(self):
        main_frame = tk.Frame(self, bg="white")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        message_label = tk.Label(
            main_frame,
            text=self.message,
            font=("Arial", 14),
            bg="white",
            wraplength=350,
        )
        message_label.pack(expand=True)

        button_frame = tk.Frame(main_frame, bg="white")
        button_frame.pack(pady=20)

        yes_button = tk.Button(
            button_frame,
            text="Yes",
            command=self._on_yes,
            width=10,
            highlightbackground="white"
        )
        yes_button.pack(side="left", padx=10)

        no_button = tk.Button(
            button_frame,
            text="No",
            command=self._on_no,
            fg="red",
            width=10,
            highlightbackground="white"
        )
        no_button.pack(side="left", padx=10)

        self.protocol("WM_DELETE_WINDOW", self._on_no)

    def _on_yes(self):
        self.result = True
        self.destroy()

    def _on_no(self):
        self.result = False
        self.destroy()

    def get_result(self):
        self.wait_window()
        return self.result