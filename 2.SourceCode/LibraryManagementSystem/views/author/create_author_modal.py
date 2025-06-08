from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QLabel, QTextEdit, QCheckBox, QSizePolicy
)
from PyQt5.QtCore import Qt
from datetime import datetime
from domain.dto.author.author_dto import AuthorDTO

class CreateAuthorModal(QDialog):
    def __init__(self, controller=None, author=None, current_user_email=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.author = author
        self.current_user_email = current_user_email or 'admin@uit.com'
        
        self.setWindowTitle("Add Author" if author is None else "Edit Author")
        self.setMinimumSize(400, 300)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.init_ui()

    def get_author(self):
        name = self.name_input.text().strip()
        if not name:
            return None
        from datetime import datetime
        from domain.dto.author.author_dto import AuthorDTO
        created_by = self.author.created_by if self.author else self.current_user_email
        update_by = self.current_user_email
        author_data = AuthorDTO(
            author_id=self.author.author_id if self.author else None,
            author_name=name,
            created_dt=self.author.created_dt if self.author else datetime.now(),
            created_by=created_by,
            update_dt=datetime.now(),
            update_by=update_by
        )
        return author_data

    def init_ui(self):
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.name_input = QLineEdit(self.author.author_name if self.author else "")
 
        form_layout.addRow("Author Name:", self.name_input)
        label = form_layout.labelForField(self.name_input)
        if label:
            label.setStyleSheet("border: none;")
        layout.addLayout(form_layout)
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)

        save_button = QPushButton("Save")
        save_button.setStyleSheet("""
            padding: 5px 15px;
            font-size: 14px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 3px;
        """)
        save_button.setMaximumWidth(150)
        save_button.clicked.connect(self.save_author)
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
        cancel_button.setMaximumWidth(150)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        button_layout.setAlignment(Qt.AlignRight)
        layout.addLayout(button_layout)

    def save_author(self):
        from lib.common_ui.confirm_modal import ConfirmModal
        from PyQt5.QtWidgets import QMessageBox
        name = self.name_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Validation Error", "Author Name is required.")
            return

        try:
            created_by = self.author.created_by if self.author else self.current_user_email
            update_by = self.current_user_email

            author_data = AuthorDTO(
                author_id=self.author.author_id if self.author else None,
                author_name=name,
                created_dt=self.author.created_dt if self.author else datetime.now(),
                created_by=created_by,
                update_dt=datetime.now(),
                update_by=update_by
            )

            # Show confirmation modal
            confirm_message = "Do you want to update this author?" if self.author else "Do you want to add this author?"
            confirm = ConfirmModal(self, message=confirm_message, title="Confirm Action")
            if confirm.exec_() == QDialog.Accepted:  # Only proceed if user clicks "Yes"
                if self.author:
                    self.controller.update_author(author_data)
                else:
                    self.controller.create_author(author_data)

                QMessageBox.information(self, "Success", "Author saved successfully.")
                self.accept()  # Close the dialog only after confirmation
            else:
                QMessageBox.information(self, "Cancelled", "Action was cancelled.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save author: {str(e)}")
