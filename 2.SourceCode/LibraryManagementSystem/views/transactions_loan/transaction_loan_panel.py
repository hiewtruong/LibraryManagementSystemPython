import tkinter as tk

class TransactionLoanPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.label = tk.Label(self, text="Quản lý đơn thuê/mượn sách", font=("Arial", 18, "bold"), bg="white")
        self.label.pack(pady=20)

    def cleanup(self):
        pass

    def destroy(self):
        self.cleanup()
        super().destroy()