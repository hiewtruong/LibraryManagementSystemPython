from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QHeaderView, QDialog, QFormLayout, QMessageBox, QSizePolicy
)
from PyQt5.QtCore import Qt
from services.category.catetory_service import GenreCategoryService
from domain.entities.genre_category import GenreCategory
from datetime import datetime

class CategoryDialog(QDialog):
    def __init__(self, parent=None, category=None, user_dto=None):
        super().__init__(parent)
        self.setWindowTitle("Add Category" if category is None else "Edit Category")
        self.service = GenreCategoryService.get_instance()
        self.category = category
        self.user_dto = user_dto
        self.init_ui()
        self.setMinimumSize(400, 250)

    def init_ui(self):
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # Form fields
        self.name_input = QLineEdit(self.category.name_category if self.category else "")
        self.name_input.setStyleSheet("padding: 5px; font-size: 14px;")
        self.genre_input = QLineEdit(self.category.genre_category if self.category else "")
        self.genre_input.setStyleSheet("padding: 5px; font-size: 14px;")

        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Genre Category:", self.genre_input)

        layout.addLayout(form_layout)

        # Buttons
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
        save_button.clicked.connect(self.save_category)
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

    def save_category(self):
        try:
            category_name = self.name_input.text().strip()
            genre_category = self.genre_input.text().strip()
            if not category_name:
                QMessageBox.warning(self, "Validation Error", "Category Name is required.")
                return

            category_data = GenreCategory(
                genre_category_id=self.category.genre_category_id if self.category else None,
                name_category=category_name,
                genre_category=genre_category,
                created_dt=self.category.created_dt if self.category else datetime.now(),
                created_by=self.user_dto.user_name if self.user_dto else "admin",
                update_dt=datetime.now(),
                update_by=self.user_dto.user_name if self.user_dto else "admin"
            )

            if self.category:
                self.service.update_category(category_data)
            else:
                self.service.add_category(category_data)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save category: {str(e)}")

class CategoryPanel(QWidget):
    def __init__(self, parent=None, user_dto=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: white;")
        self.parent = parent
        self.user_dto = user_dto
        self.service = GenreCategoryService.get_instance()
        self.init_ui()
        self.setMinimumSize(1370, 830)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Title
        title_label = QLabel("Manage Categories")
        title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            padding: 10px;
            border: none;
            background-color: none;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Search bar and Add New button
        search_layout = QHBoxLayout()

        # Search components
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search categories...")
        self.search_input.setStyleSheet("padding: 5px; font-size: 14px;")
        search_layout.addWidget(self.search_input)

        search_button = QPushButton("Search")
        search_button.setStyleSheet("""
            padding: 5px 15px;
            font-size: 14px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 3px;
        """)
        search_button.clicked.connect(self.search_categories)
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
        add_button.clicked.connect(self.add_category)
        search_layout.addStretch()
        search_layout.addWidget(add_button)

        layout.addLayout(search_layout)

        # Category table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Genre Category", "Created Dt", "Created By", "Actions"])
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 5px;
                border: 1px solid #ddd;
            }
        """)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        self.load_categories()

    def load_categories(self, categories=None):
        if categories is None:
            categories = self.service.find_all()

        self.table.setRowCount(len(categories))
        for row, category in enumerate(categories):
            self.table.setItem(row, 0, QTableWidgetItem(str(category.genre_category_id)))
            self.table.setItem(row, 1, QTableWidgetItem(category.name_category or ""))
            self.table.setItem(row, 2, QTableWidgetItem(category.genre_category or ""))
            self.table.setItem(row, 3, QTableWidgetItem(category.created_dt.strftime("%Y-%m-%d %H:%M:%S") if category.created_dt else ""))
            self.table.setItem(row, 4, QTableWidgetItem(category.created_by or ""))

            # Action buttons
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(5)

            edit_button = QPushButton("Edit")
            edit_button.setStyleSheet("""
                padding: 3px 10px;
                font-size: 12px;
                background-color: #FFC107;
                color: white;
                border: none;
                border-radius: 3px;
            """)
            edit_button.clicked.connect(lambda _, c=category: self.edit_category(c))
            action_layout.addWidget(edit_button)

            delete_button = QPushButton("Delete")
            delete_button.setStyleSheet("""
                padding: 3px 10px;
                font-size: 12px;
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 3px;
            """)
            delete_button.clicked.connect(lambda _, c=category.genre_category_id: self.delete_category(c))
            action_layout.addWidget(delete_button)

            self.table.setCellWidget(row, 5, action_widget)

    def search_categories(self):
        search_term = self.search_input.text().strip().lower()
        if not search_term:
            self.load_categories()
            return

        categories = self.service.find_all()
        filtered_categories = [
            category for category in categories
            if (search_term in (category.name_category or "").lower() or
                search_term in (category.genre_category or "").lower())
        ]
        self.load_categories(filtered_categories)

    def add_category(self):
        dialog = CategoryDialog(self, None, self.user_dto)
        if dialog.exec_():
            self.load_categories()

    def edit_category(self, category):
        dialog = CategoryDialog(self, category, self.user_dto)
        if dialog.exec_():
            self.load_categories()

    def delete_category(self, category_id):
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this category?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                self.service.delete_category(category_id)
                self.load_categories()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete category: {str(e)}")