from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QLabel, QSizePolicy, QComboBox
)
from PyQt5.QtCore import Qt
from datetime import datetime
from domain.dto.user.user_dto import UserDTO
from services.user.user_service import UserService

class CreateUserModal(QDialog):
    def __init__(self, controller=None, user=None, parent=None, current_user_email=None):
        super().__init__(parent)
        self.user = user
        self.controller = controller
        self.user_service = UserService.get_instance()
        self.current_user_email = current_user_email
        
        self.setWindowTitle("Add User" if user is None else "Edit User")
        self.setMinimumSize(400, 400)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.username_input = QLineEdit(self.user.user_name if self.user else "")
        form_layout.addRow("Username:", self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        if self.user:
            self.password_input.setText(self.user.password if hasattr(self.user, 'password') else "")
        form_layout.addRow("Password:", self.password_input)

        self.email_input = QLineEdit(self.user.email if self.user else "")
        form_layout.addRow("Email:", self.email_input)

        self.first_name_input = QLineEdit(self.user.first_name if self.user else "")
        form_layout.addRow("First Name:", self.first_name_input)

        self.last_name_input = QLineEdit(self.user.last_name if self.user else "")
        form_layout.addRow("Last Name:", self.last_name_input)

        self.phone_input = QLineEdit(self.user.phone if self.user else "")
        form_layout.addRow("Phone:", self.phone_input)

        self.address_input = QLineEdit(self.user.address if self.user else "")
        form_layout.addRow("Address:", self.address_input)

        # Gender combobox
        self.gender_combobox = QComboBox()
        self.gender_combobox.addItems(["Female", "Male"])

        # Set initial state if editing user
        if self.user and hasattr(self.user, 'gender'):
            if self.user.gender == 1:
                self.gender_combobox.setCurrentText("Male")
            else:
                self.gender_combobox.setCurrentText("Female")

        form_layout.addRow("Gender:", self.gender_combobox)

        # User role combobox
        self.user_role_combobox = QComboBox()
        self.user_roles = self.user_service.get_all_user_roles()
        for role in self.user_roles:
            self.user_role_combobox.addItem(role.role_name, role.user_role_id_fk)

        # Set initial user role if editing user
        if self.user and hasattr(self.user, 'user_role_id'):
            index = self.user_role_combobox.findData(self.user.user_role_id)
            if index >= 0:
                self.user_role_combobox.setCurrentIndex(index)
        else:
            # Default to first role
            self.user_role_combobox.setCurrentIndex(0)

        form_layout.addRow("User Role:", self.user_role_combobox)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.setStyleSheet("""
            padding: 5px 15px;
            font-size: 14px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 3px;
        """)
        save_button.clicked.connect(self.save_user)
        button_layout.addWidget(save_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("""
            padding: 5px 15px;
            font-size: 14px;
            background-color: #F44336;
            color: white;
            border: none;
            border-radius: 3px;
        """)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

    def save_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        email = self.email_input.text().strip()
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        phone = self.phone_input.text().strip()
        address = self.address_input.text().strip()

        # Determine gender from combobox and map to int
        gender_text = self.gender_combobox.currentText()
        gender = 1 if gender_text == "Male" else 0

        # Get user role id from combobox
        user_role_id = self.user_role_combobox.currentData()

        if not username:
            QMessageBox.warning(self, "Validation Error", "Username is required.")
            return
        if not password and not self.user:
            QMessageBox.warning(self, "Validation Error", "Password is required.")
            return
        if not email:
            QMessageBox.warning(self, "Validation Error", "Email is required.")
            return
        if not phone:
            QMessageBox.warning(self, "Validation Error", "Phone is required.")
            return
        if gender_text not in ["Male", "Female"]:
            QMessageBox.warning(self, "Validation Error", "Gender is required.")
            return
        if user_role_id is None:
            QMessageBox.warning(self, "Validation Error", "User role is required.")
            return

        try:
            # Check for duplicate email before creating or updating
            if not self.user or (self.user and self.user.email != email):
                if self.controller.is_email_duplicate(email):
                    QMessageBox.warning(self, "Validation Error", "Email already exists.")
                    return

                created_by = self.user.created_by if self.user else self.current_user_email
                update_by = self.current_user_email

            user_data = UserDTO(
                user_id=self.user.user_id if self.user else None,
                user_name=username,
                password=password if password else (self.user.password if self.user else None),
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                address=address,
                gender=gender,
                user_role_id=user_role_id,
                is_delete=self.user.is_delete if self.user else 0,
                created_dt=self.user.created_dt if self.user else datetime.now(),
                created_by=self.current_user_email,
                update_dt=datetime.now(),
                update_by=self.current_user_email
            )

            if self.user:
                self.controller.update_user(user_data)
            else:
                self.controller.create_user(user_data)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save user: {str(e)}")
