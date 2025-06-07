from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt
from lib.common_ui.confirm_modal import ConfirmModal
from lib.notifier_utils import show_success, show_warning

class UserPanel(QWidget):
    def __init__(self, controller=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.initUI()
        self.setMinimumSize(1370, 830)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

    def initUI(self):
        self.setWindowTitle("Manage Users")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 10, 10)
        main_layout.setSpacing(10)

        # Title label
        title_label = QLabel("Manage Users")
        title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            border: none;
            padding-top: 10px;
            background-color: none;
        """)
        title_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(title_label)

        # Search bar and Add New button
        search_layout = QHBoxLayout()
        search_layout.setAlignment(Qt.AlignLeft)

        # Search label
        search_label = QLabel("Search")
        search_label_font = title_label.font()
        search_label_font.setPixelSize(13)
        search_label.setFont(search_label_font)
        search_label.setStyleSheet("border: none;")
        search_label.setMaximumWidth(50)
        search_layout.addWidget(search_label)

        # Search field combo box
        self.search_field = QComboBox()
        self.search_field.addItems(["User Name", "Email", "First Name", "Last Name"])
        self.search_field.setMaximumWidth(180)
        self.search_field.setMinimumHeight(25)
        combo_font = self.search_field.font()
        combo_font.setPixelSize(13)
        self.search_field.setFont(combo_font)
        search_layout.addWidget(self.search_field)

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search term...")
        self.search_input.setMaximumWidth(250)
        self.search_input.setMinimumHeight(25)
        self.search_input.setFont(combo_font)
        search_layout.addWidget(self.search_input)

        # Search button
        search_button = QPushButton("Search")
        search_button.setFixedWidth(70)
        search_button.setFixedHeight(25)
        search_button.setStyleSheet("""
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
        """)
        search_button.clicked.connect(self.search_users)
        search_layout.addWidget(search_button)

        # Add New button (optional reposition or remove)
        # Here, I will keep it but move it to the right side with stretch
        search_layout.addStretch()
        add_button = QPushButton("Add New")
        add_button.setFixedHeight(25)
        add_button.setStyleSheet("""
            background-color: #2196F3;
            color: white;
            border-radius: 5px;
        """)
        add_button.clicked.connect(self.create_new_user)
        search_layout.addWidget(add_button)

        main_layout.addLayout(search_layout)

        # User table
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(11)
        self.user_table.setHorizontalHeaderLabels([
            "UserID", "UserName", "Email", "FirstName", "LastName", "Phone", "Address", "Password", "Gender", "Edit", "Delete"
        ])
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.user_table.horizontalHeader().setStretchLastSection(True)
        self.user_table.verticalHeader().setVisible(False)
        self.user_table.setAlternatingRowColors(True)
        self.user_table.setStyleSheet("""
            alternate-background-color: #f9f9f9;
            background-color: white;
            border: 0.5px solid;
        """)
        self.user_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.user_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.user_table.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # Set font sizes for header and data
        font_header = self.user_table.horizontalHeader().font()
        font_header.setPixelSize(15)
        font_header.setBold(True)
        self.user_table.horizontalHeader().setFont(font_header)

        font_data = self.user_table.font()
        font_data.setPixelSize(13)
        font_data.setBold(False)
        self.user_table.setFont(font_data)

        main_layout.addWidget(self.user_table)

        # Bottom panel with total label (optional adjust or remove)
        bottom_panel = QHBoxLayout()
        bottom_panel.addStretch()
        self.total_label = QLabel("Total: 0")
        bottom_panel.addWidget(self.total_label)
        main_layout.addLayout(bottom_panel)

        # Load all users on init
        if self.controller:
            users = self.controller.get_all_users()
            self.load_user_data(users)

    def load_user_data(self, users):
        filtered_users = [user for user in users if not getattr(user, 'is_delete', False)]
        self.user_table.setRowCount(len(filtered_users))
        for row, user in enumerate(filtered_users):
            self.user_table.setItem(row, 0, QTableWidgetItem(str(getattr(user, 'user_id', ''))))
            self.user_table.setItem(row, 1, QTableWidgetItem(getattr(user, 'user_name', '')))
            self.user_table.setItem(row, 2, QTableWidgetItem(getattr(user, 'email', '')))
            self.user_table.setItem(row, 3, QTableWidgetItem(getattr(user, 'first_name', '')))
            self.user_table.setItem(row, 4, QTableWidgetItem(getattr(user, 'last_name', '')))
            self.user_table.setItem(row, 5, QTableWidgetItem(getattr(user, 'phone', '')))
            self.user_table.setItem(row, 6, QTableWidgetItem(getattr(user, 'address', '')))
            self.user_table.setItem(row, 7, QTableWidgetItem(getattr(user, 'password', '')))
            self.user_table.setItem(row, 8, QTableWidgetItem(str(getattr(user, 'gender', ''))))

            # Action buttons
            action_widget_edit = QPushButton("Edit")
            action_widget_edit.setStyleSheet("""
                height: 25px;
                font-size: 12px;
                background-color: #FFC107;
                color: white;
                border: none;
                border-radius: 3px;
            """)
            action_widget_edit.clicked.connect(lambda _, u=user: self.edit_user(u))

            action_widget_delete = QPushButton("Delete")
            action_widget_delete.setStyleSheet("""
                height: 25px;
                font-size: 12px;
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 3px;
            """)
            action_widget_delete.clicked.connect(lambda _, u_id=user.user_id: self.delete_user(u_id))

            self.user_table.setCellWidget(row, 9, action_widget_edit)
            self.user_table.setCellWidget(row, 10, action_widget_delete)

        self.total_label.setText(f"Total: {len(filtered_users)}")

    def search_users(self):
        search_field = self.search_field.currentText().lower().replace(" ", "_")
        search_term = self.search_input.text().strip().lower()
        if not search_term:
            if self.controller:
                users = self.controller.get_all_users()
                self.load_user_data(users)
            return

        if self.controller:
            users = self.controller.get_all_users()
            filtered_users = [
                user for user in users
                if search_term in str(getattr(user, search_field, "")).lower()
            ]
            self.load_user_data(filtered_users)
        else:
            show_warning(self, "Controller not set.")

    def create_new_user(self):
        if self.controller:
            from views.user.create_user_modal import CreateUserModal
            dialog = CreateUserModal(controller=self.controller, parent=self)
            if dialog.exec_():
                users = self.controller.get_all_users()
                self.load_user_data(users)
                if hasattr(self.controller, 'notify_user_added'):
                    self.controller.notify_user_added()
        else:
            if hasattr(self.controller, 'notify_controller_missing'):
                self.controller.notify_controller_missing()

    def edit_user(self, user):
        if self.controller:
            from views.user.create_user_modal import CreateUserModal
            dialog = CreateUserModal(controller=self.controller, user=user, parent=self)
            if dialog.exec_():
                users = self.controller.get_all_users()
                self.load_user_data(users)
                if hasattr(self.controller, 'notify_user_updated'):
                    self.controller.notify_user_updated()
        else:
            if hasattr(self.controller, 'notify_controller_missing'):
                self.controller.notify_controller_missing()

    def delete_user(self, user_id):
        if self.controller and hasattr(self.controller, 'confirm_user_deletion'):
            confirmed = self.controller.confirm_user_deletion(user_id)
            if confirmed:
                success = self.controller.delete_user(user_id)
                if success:
                    users = self.controller.get_all_users()
                    self.load_user_data(users)
                    if hasattr(self.controller, 'notify_user_deleted'):
                        self.controller.notify_user_deleted()
                else:
                    if hasattr(self.controller, 'notify_user_delete_failed'):
                        self.controller.notify_user_delete_failed()
            else:
                if hasattr(self.controller, 'notify_controller_missing'):
                    self.controller.notify_controller_missing()
