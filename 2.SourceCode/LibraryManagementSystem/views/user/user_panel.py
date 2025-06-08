
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QComboBox, QHeaderView, QSizePolicy, QMessageBox, QDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from services.user.user_service import UserService

from lib.common_ui.confirm_modal import ConfirmModal
class UserPanel(QWidget):
    def __init__(self, parent=None, user_dto=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: white;")
        self.parent = parent
        self.user_dto = user_dto
        from controllers.user_controller import UserController
        self.controller = UserController(user_service=UserService.get_instance())
        self.service = UserService.get_instance()
        self.init_ui()
        self.setMinimumSize(1370, 830)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 10, 10, 10)
        layout.setSpacing(5)

        # Title
        title_label = QLabel("Manage Users")
        title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            padding: 10px;
            border: none;
            background-color: none;
        """)
        title_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(title_label)

        # Search bar and Add New button
        search_layout = QHBoxLayout()

        # Search label
        search_label = QLabel("Search:")
        search_label_font = QFont()
        search_label_font.setPixelSize(13)
        search_label.setFont(search_label_font)
        search_label.setStyleSheet("border: none;")
        search_label.setMaximumWidth(50)
        search_layout.addWidget(search_label)

        # Search components
        self.search_field = QComboBox()
        self.search_field.setMaximumWidth(180)
        self.search_field.setMinimumHeight(25)
        self.search_field.setMinimumWidth(150)
        self.search_field.addItems(["User Name", "Email", "First Name", "Last Name"])
        self.search_field.setStyleSheet("padding: 5px; font-size: 13px;border: 0.5px solid;")
        search_layout.addWidget(self.search_field)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search term...")
        self.search_input.setFixedSize(250, 25)
        search_layout.addWidget(self.search_input)

        search_button = QPushButton("Search")
        search_button.setStyleSheet("""
            padding: 5px 15px;
            font-size: 13px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 3px;
        """)
        search_button.clicked.connect(self.search_users)
        search_layout.addWidget(search_button)

        # Add New button
        add_button = QPushButton("Add New")
        add_button.setStyleSheet("""
            padding: 5px 15px;
            font-size: 14px;
            background-color: #2196F3;
            color: white;
            border: none;
            border-radius: 3px;
        """)
        add_button.clicked.connect(self.add_user)
        search_layout.addStretch()
        search_layout.addWidget(add_button)

        layout.addLayout(search_layout)

        # User table
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setFont(QFont("Arial", 13))
        self.table.setRowHeight(0, 20)
        self.table.setShowGrid(True)
        self.table.setHorizontalHeaderLabels([
            "UserID", "UserName", "Email", "FirstName", "LastName", "Phone", "Address", "Password", "Gender", "Actions"
        ])
        self.table.setStyleSheet("""
            border: 0.5px solid;
            font-size: 12px;
        """)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.doubleClicked.connect(self.handle_double_click)

        header_font = QFont()
        header_font.setPixelSize(13)
        header_font.setBold(True)
        for i in range(self.table.columnCount()):
            header_item = self.table.horizontalHeaderItem(i)
            if header_item:
                header_item.setFont(header_font)
        layout.addWidget(self.table)

        self.load_users()

    def load_users(self, users=None):
        if users is None:
            users = self.service.get_all_users()

        filtered_users = [user for user in users if not getattr(user, 'is_delete', False)]
        self.table.setRowCount(len(filtered_users))
        for row, user in enumerate(filtered_users):
            self.table.setItem(row, 0, QTableWidgetItem(str(user.user_id)))
            self.table.setItem(row, 1, QTableWidgetItem(user.user_name))
            self.table.setItem(row, 2, QTableWidgetItem(user.email))
            self.table.setItem(row, 3, QTableWidgetItem(user.first_name))
            self.table.setItem(row, 4, QTableWidgetItem(user.last_name))
            self.table.setItem(row, 5, QTableWidgetItem(user.phone))
            self.table.setItem(row, 6, QTableWidgetItem(user.address))
            self.table.setItem(row, 7, QTableWidgetItem(user.password))
            self.table.setItem(row, 8, QTableWidgetItem(str(user.gender)))

            # Action buttons (only Delete button)
            action_widget = QWidget()
            action_widget.setStyleSheet("border: none; background-color: transparent;")
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(5)

            delete_button = QPushButton("Delete")
            delete_button.setStyleSheet("""
                padding: 3px 10px;
                font-size: 12px;
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 3px;
            """)
            delete_button.setMaximumWidth(80)
            delete_button.clicked.connect(lambda _, u_id=user.user_id: self.delete_user(u_id))
            action_layout.addWidget(delete_button)

            self.table.setCellWidget(row, 9, action_widget)

    def handle_double_click(self, index):
        row = index.row()
        user_id = int(self.table.item(row, 0).text())
        user = self.service.get_user_by_id(user_id)  # Ensure this method exists in UserService
        if user:
                self.edit_user(user)
        else:
             QMessageBox.warning(self, "Error", f"User with ID {user_id} not found.")

    def search_users(self):
        search_field = self.search_field.currentText().lower().replace(" ", "_")
        search_term = self.search_input.text().strip().lower()
        if not search_term:
            self.load_users()
            return

        users = self.service.get_all_users()
        filtered_users = [
            user for user in users
            if search_term in str(getattr(user, search_field, "")).lower()
        ]
        self.load_users(filtered_users)

    def add_user(self):
        from views.user.create_user_modal import CreateUserModal
        dialog = CreateUserModal(controller=self.service, parent=self, current_user_email=self.user_dto.email if self.user_dto else None)
        if dialog.exec_():
           self.load_users()

    def edit_user(self, user):
        from views.user.create_user_modal import CreateUserModal
        dialog = CreateUserModal(controller=self.service, user=user, parent=self, current_user_email=self.user_dto.email if self.user_dto else None)
        if dialog.exec_():
                self.load_users()

    def delete_user(self, user_id):
       
        confirm = ConfirmModal(self, message="Are you sure you want to delete this user?", title="Confirm Delete")
        if confirm.exec_() == QDialog.Accepted:
            if self.service.delete_user(user_id):
                self.load_users()
