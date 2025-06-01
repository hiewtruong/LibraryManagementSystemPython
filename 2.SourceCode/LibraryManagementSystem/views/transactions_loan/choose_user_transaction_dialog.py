from typing import List
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QFrame, QMessageBox, QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from domain.dto.user.user_role_dto import UserRoleDTO
from lib.notifier_utils import show_warning

class TransactionUserChooseModal(QDialog):
    def __init__(self, parent, user_list: List[UserRoleDTO]):
        super().__init__(parent)
        self.parent = parent
        self.user_list = user_list
        self.selected_user = None
        self.setWindowTitle("Choose User")
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(550, 250)
        main_layout = QVBoxLayout(self)
        self.table = QTableWidget() 
        self.table.setStyleSheet("""
            QTableWidget {
                border: 0.5px solid gray;
                border-radius: 5px;
                background-color: #f2f2f2;
            }
        """)
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["User ID", "User Name", "Email"])
        self.table.setRowCount(len(self.user_list))
        self.table.setFont(QFont("Arial", 12))
        self.table.horizontalHeader().setFont(QFont("Arial", 13, QFont.Bold))
        self.table.setRowHeight(0, 15)
        self.table.setShowGrid(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 250) 
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch) 

        for row, user in enumerate(self.user_list):
            self.table.setRowHeight(row, 25)
            user_id_item = QTableWidgetItem(str(user.user_id))
            user_id_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 0, user_id_item)
            self.table.setItem(row, 1, QTableWidgetItem(user.user_name))
            self.table.setItem(row, 2, QTableWidgetItem(user.email))
        self.table.itemSelectionChanged.connect(self.update_selected_user)

        main_layout.addWidget(self.table)

        footer_panel = QHBoxLayout()
        footer_panel.setAlignment(Qt.AlignRight)
        footer_panel.setContentsMargins(10, 5, 10, 5)  
        btn_select = QPushButton("Choose User")
        btn_select.setFixedWidth(90)
        btn_select.setFixedHeight(25)
        btn_select.setStyleSheet("""
            background-color: blue;
            color: white;
            border-radius: 5px;
        """)
        btn_select.clicked.connect(self.select_user)
        footer_panel.addWidget(btn_select)
        main_layout.addLayout(footer_panel)

    def update_selected_user(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            self.selected_user = self.user_list[row]
        else:
            self.selected_user = None

    def select_user(self):
        if self.selected_user is None:
            show_warning(parent=self, message="Please select a user.")
        else:
            self.accept()   

    def get_selected_user(self):
        return self.selected_user