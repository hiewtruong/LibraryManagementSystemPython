from typing import List
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QFrame, QMessageBox, QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from domain.dto.transaction.transaction_loan_detail_dto import TransactionLoanDetailDTO
from domain.dto.transaction.transaction_loan_detail_request_dto import TransactionLoanDetailRequestDTO
from domain.dto.transaction.transaction_loan_header_dto import TransactionLoanHeaderDTO
from domain.dto.transaction.transaction_loan_header_revoke_dto import TransactionLoanHeaderRevokeDTO
from lib.common_ui.confirm_modal import ConfirmModal
from lib.common_ui.notification_modal import NotificationModal
from lib.constants import TRANS_BORROW
from lib.date_utils import format_date_mmddyyyy
from lib.notifier_utils import show_error, show_success

class TransactionLoanDetailDialog(QDialog):
    reloadDataSignal = QtCore.pyqtSignal()
    def __init__(self, parent, container, header_data: TransactionLoanHeaderDTO, details_data: List[TransactionLoanDetailDTO]):
        super().__init__(parent)
        self.container = container 
        self.parent = parent
        self.setWindowTitle(f"Transaction Loan Details - {header_data.loan_ticket_number}")
        self.setModal(True)
        self.header_data = header_data
        self.details_data = details_data
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(800, 450)
        main_layout = QVBoxLayout(self)

        header_panel = QFrame()
        header_panel.setStyleSheet("""
            QFrame {
                border: 2px solid gray;
                border-radius: 5px;
            }
        """)
        header_layout = QVBoxLayout(header_panel)
        header_layout.setContentsMargins(20, 20, 20, 20)
        normal_font = QFont("Arial", 12)

        label_pairs = [
            ("Loan Ticket Number", self.header_data.loan_ticket_number),
            ("UserName", self.header_data.use_name),
            ("Email", self.header_data.email),
            ("Phone", self.header_data.phone),
            ("Total Books", self.header_data.total_qty),
            ("Loan Date", format_date_mmddyyyy(self.header_data.loan_dt)),
            ("Return Date", format_date_mmddyyyy(self.header_data.loan_return_dt)),
            ("Status", self.header_data.status_name)
        ]

        for i in range(0, len(label_pairs), 2):
            row_layout = QHBoxLayout()
            for label_text, value in label_pairs[i:i+2]:
                label = QLabel(f"<b>{label_text}:</b> {value}")
                label.setFont(normal_font)
                label.setStyleSheet("border: none;")
                row_layout.addWidget(label, stretch=1)
            for _ in range(2 - len(label_pairs[i:i+2])):
                row_layout.addStretch(1)
            header_layout.addLayout(row_layout)

        main_layout.addWidget(header_panel)

        table = QTableWidget()
        table.setStyleSheet("""
            QTableWidget {
                border: 0.5px solid gray;
                border-radius: 5px;
            }
        """)
        table.verticalHeader().setVisible(False)
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["No#", "Title", "Author", "Category"])
        table.setRowCount(len(self.details_data))
        table.setFont(QFont("Arial", 12))
        table.horizontalHeader().setFont(QFont("Arial", 13, QFont.Bold)) 

        for row in range(len(self.details_data)):
            table.setRowHeight(row, 22)

        table.setColumnWidth(0, 50)
        table.setColumnWidth(1, 250)
        table.setColumnWidth(2, 150)
        table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)

        for row, detail in enumerate(self.details_data):
            item_no = QTableWidgetItem(str(row + 1))
            item_no.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            table.setItem(row, 0, item_no)

            table.setItem(row, 1, QTableWidgetItem(str(getattr(detail, 'title', ''))))
            table.setItem(row, 2, QTableWidgetItem(str(getattr(detail, 'author', ''))))
            table.setItem(row, 3, QTableWidgetItem(str(getattr(detail, 'genre_category', ''))))

        main_layout.addWidget(table)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignRight)

        if self.header_data.status == TRANS_BORROW:
            revoke_button = QPushButton("Revoke")
            revoke_button.setFixedWidth(70)
            revoke_button.setFixedHeight(25)
            revoke_button.setStyleSheet("""
                background-color: blue;
                color: white;
                border-radius: 5px;
            """)
            revoke_button.clicked.connect(self.revoke_transaction)
            button_layout.addWidget(revoke_button)

        if self.header_data.expired == 1:
            remid_button = QPushButton("Remind/Send Email")
            remid_button.setFixedWidth(120)
            remid_button.setFixedHeight(25)
            remid_button.setStyleSheet("""
                background-color: red;
                color: white;
                border-radius: 5px;
            """)
            remid_button.clicked.connect(self.remind_transaction)
            button_layout.addWidget(remid_button)

        main_layout.addLayout(button_layout)

    def revoke_transaction(self):
        from controllers.transaction_loan_controller import TransactionLoanController
        controller = TransactionLoanController()
        modal = ConfirmModal(self, message="Would you like to confirm the return of this book?", title="Revoke")
        if modal.exec_() == QtWidgets.QDialog.Accepted:
            request_loan = TransactionLoanHeaderRevokeDTO(loan_header_id=self.header_data.loan_header_id)
            for detail in self.details_data:
                detail_request = TransactionLoanDetailRequestDTO()
                detail_request.load_book_id = detail.loan_book_id
                request_loan.loan_details.append(detail_request)
            is_success = controller.revoke_transaction(request_loan)
            if is_success == True:
                controller.send_email_revoke_transaction_loan(self.header_data.loan_header_id)
                show_success(parent=self.parent,message="Revoke this trans successfully")
                self.reloadDataSignal.emit()
                self.close()
            else:
                show_error(parent=None,message="Can't revoke this trans. Please try again!")

    def remind_transaction(self):
        from controllers.transaction_loan_controller import TransactionLoanController
        modal = ConfirmModal(self, message="Would you like to send an email to remind this trans?", title="Remind")
        controller = TransactionLoanController()
        if modal.exec_() == QtWidgets.QDialog.Accepted:
            controller.send_email_remind_transaction_loan(self.header_data.loan_header_id)
            show_success(parent=self.parent,message="Remind this trans successfully")
            self.reloadDataSignal.emit()
            self.close()
    
    def close_dialog(self):
        self.reloadDataSignal.emit()
        self.close()