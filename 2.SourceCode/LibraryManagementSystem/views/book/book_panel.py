from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QComboBox, QHeaderView, QDialog, QFormLayout,
    QMessageBox, QCheckBox, QSpinBox, QSizePolicy, QFileDialog, QListWidget, QListWidgetItem, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5 import QtWidgets
from services.book.book_service import BookService
from services.category.catetory_service import GenreCategoryService
from services.author.author_service import AuthorService
from domain.entities.book import Book
from datetime import datetime
import os
import shutil
from lib.common_ui.confirm_modal import ConfirmModal
from lib.notifier_utils import show_error, show_success

class BookDialog(QDialog):
    def __init__(self, parent=None, book=None, user_dto=None):
        super().__init__(parent)
        self.setWindowTitle("Add Book" if book is None else "Edit Book")
        self.service = BookService.get_instance()
        self.category_service = GenreCategoryService.get_instance()
        self.author_service = AuthorService.get_instance()
        self.book = book
        self.user_dto = user_dto
        self.parent = parent
        self.init_ui()
        self.setMinimumSize(640, 780)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet("border: none;font-size: 12px;border-radius: 6px;font-weight: 500;")

    def init_ui(self):
        self.all_categories = self.category_service.get_all_genre_categories()
        self.all_authors = self.author_service.get_all_authors()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 10, 10, 10)
        layout.setSpacing(5)
        form_layout = QFormLayout()

        # Form fields
        self.title_input = QLineEdit(self.book.title if self.book else "")
        self.title_input.setStyleSheet("border: 0.5px solid; padding: 2px;margin-bottom: 10px;")

        # Author selection
        self.author_combo = QComboBox()
        self.author_combo.addItems([author.author_name for author in self.all_authors])
        self.author_combo.setStyleSheet("border: 0.5px solid; padding: 2px;margin-bottom: 10px;")
        if self.book and self.book.author:
            self.author_combo.setCurrentText(self.book.author)

        # Genre category multiple selection
        self.genre_list = QListWidget()
        self.genre_list.setSelectionMode(QListWidget.MultiSelection)
        self.genre_list.setStyleSheet("border: 0.5px solid; padding: 2px;margin-bottom: 10px;")
        for category in self.all_categories:
            item = QListWidgetItem(category.name_category)
            item.setData(Qt.UserRole, category.genre_category_id)
            self.genre_list.addItem(item)
        if self.book and self.book.genre_category:
            selected_ids = self.book.genre_category.split(",")
            for item in [self.genre_list.item(i) for i in range(self.genre_list.count())]:
                if str(item.data(Qt.UserRole)) in selected_ids:
                    item.setSelected(True)
        self.genre_list.setMinimumHeight(100)  # Ensure list is visible

        self.publisher_input = QLineEdit(self.book.publisher if self.book else "")
        self.publisher_input.setStyleSheet("border: 0.5px solid; padding: 2px;margin-bottom: 10px;")
        self.year_input = QSpinBox()
        self.year_input.setStyleSheet("border: 0.5px solid; padding: 2px;margin-bottom: 10px;")
        self.year_input.setRange(1000, 9999)
        publish_year = self.book.publish_year.year if self.book and self.book.publish_year else 2025
        self.year_input.setValue(publish_year)
        self.location_input = QLineEdit(self.book.location if self.book else "")
        self.location_input.setStyleSheet("border: 0.5px solid; padding: 2px;margin-bottom: 10px;")
        self.display_check = QCheckBox()
        self.display_check.setChecked(self.book.is_display if self.book else False)
        self.display_check.setStyleSheet("margin-bottom: 10px;")
        self.qty_oh_input = QSpinBox()
        self.qty_oh_input.setRange(0, 1000)
        self.qty_oh_input.setValue(self.book.qty_oh if self.book else 0)
        self.qty_oh_input.setStyleSheet("border: 0.5px solid; padding: 2px;margin-bottom: 10px;")
        self.cover_path = self.book.cover if self.book else ""
        self.cover_button = QPushButton("Select Cover Image")
        self.cover_button.clicked.connect(self.select_image)
        self.cover_button.setStyleSheet("border: 0.5px solid #ccc; padding: 5px;margin-bottom: 10px;background-color: #35f36b;")
        self.hashtag_input = QLineEdit(self.book.hashtag if self.book else "")
        self.hashtag_input.setStyleSheet("border: 0.5px solid; padding: 2px;margin-bottom: 10px;")
        self.landing_page_input = QTextEdit()
        self.landing_page_input.setMinimumHeight(60)  # Ensure textarea is visible
        self.landing_page_input.setText(self.book.landing_page if self.book else "")
        self.landing_page_input.setStyleSheet("border: 0.5px solid; padding: 2px;margin-bottom: 10px;")
        self.hashtag_input.setStyleSheet("border: 0.5px solid; padding: 2px;margin-bottom: 10px;")

        # Image display
        self.image_label = QLabel()
        self.image_label.setFixedSize(150, 200)
        self.image_label.setStyleSheet("border: 0.5px solid; padding: 2px;margin-bottom: 10px;")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.update_image()

        form_layout.addRow(self.cover_button, self.image_label)
        form_layout.addRow("Title:", self.title_input)
        form_layout.addRow("Author:", self.author_combo)
        form_layout.addRow("Publisher:", self.publisher_input)
        form_layout.addRow("Publish Year:", self.year_input)
        form_layout.addRow("Genre Categories:", self.genre_list)
        form_layout.addRow("Location:", self.location_input)
        form_layout.addRow("Display:", self.display_check)
        form_layout.addRow("Quantity On Hand:", self.qty_oh_input)
        form_layout.addRow("Hashtag:", self.hashtag_input)
        form_layout.addRow("Landing Page:", self.landing_page_input)

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
        save_button.clicked.connect(self.save_book)
        save_button.setMaximumWidth(150)
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

    def select_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Cover Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_name:
            # Define destination folder
            dest_folder = "resources/img"
            os.makedirs(dest_folder, exist_ok=True)
            # Generate unique filename
            base_name = os.path.basename(file_name)
            dest_path = os.path.join(dest_folder, base_name)
            counter = 1
            name, ext = os.path.splitext(base_name)
            while os.path.exists(dest_path):
                dest_path = os.path.join(dest_folder, f"{name}_{counter}{ext}")
                counter += 1
            # Copy file to destination
            shutil.copy(file_name, dest_path)
            # remove path "resources/img/" from dest_path
            dest_path = dest_path.replace(dest_folder + "\\", "")
            self.cover_path = dest_path
            self.update_image()

    def update_image(self):
        if self.cover_path:
            pixmap = QPixmap("resources/img/" + self.cover_path)
            if pixmap.isNull():
                self.image_label.setText("Invalid image")
            else:
                self.image_label.setPixmap(pixmap.scaled(150, 200, Qt.KeepAspectRatio))
        else:
            self.image_label.setText("No image")

    def save_book(self):
        try:
            # Convert selected categories to comma-separated IDs
            selected_items = self.genre_list.selectedItems()
            genre_ids = [str(item.data(Qt.UserRole)) for item in selected_items]
            genre_category = ",".join(genre_ids) if genre_ids else ""

            book_data = Book(
                book_id=self.book.book_id if self.book else None,
                title=self.title_input.text().strip(),
                author=self.author_combo.currentText().strip(),
                publisher=self.publisher_input.text().strip(),
                genre_category=genre_category,
                publish_year=self.year_input.value(),
                location=self.location_input.text().strip(),
                is_display=self.display_check.isChecked(),
                qty_oh=self.qty_oh_input.value(),
                cover=self.cover_path,
                hashtag=self.hashtag_input.text().strip(),
                landing_page=self.landing_page_input.toPlainText().strip(),
                created_dt=self.book.created_dt if self.book else datetime.now(),
                created_by=self.book.created_by if self.book else "admin",
                update_dt=datetime.now(),
                update_by=self.user_dto.user_name if self.user_dto else "admin"
            )

            if not book_data.title or not book_data.author:
                # QMessageBox.warning(self, "Validation Error", "Title and Author are required fields.")
                show_error(parent=self.parent, message="Title and Author are required fields.")
                return

            modal = ConfirmModal(self, message="Are you sure you want to save this book?", title="Confirm Save")
            if modal.exec_() == QtWidgets.QDialog.Accepted:
                if self.book:
                    self.service.update_book(book_data)
                else:
                    self.service.add_book(book_data)
                self.accept()
                show_success(parent=self.parent,message="Book saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save book: {str(e)}")

class BookPanel(QWidget):
    def __init__(self, parent=None, user_dto=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: white;")
        self.parent = parent
        self.user_dto = user_dto
        self.service = BookService.get_instance()
        self.init_ui()
        self.setMinimumSize(1370, 830)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 10, 10, 10)
        layout.setSpacing(5)

        # Title
        title_label = QLabel("Manage Books")
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
        search_label = QLabel("Search")
        search_label_font = QFont()
        search_label_font.setPixelSize(13)
        search_label.setFont(search_label_font)
        search_label.setStyleSheet("border: none;padding-right: 10px;")
        search_label.setMaximumWidth(80)
        search_layout.addWidget(search_label)
        
        # Search components
        self.search_field = QComboBox()
        self.search_field.setMaximumWidth(180)
        self.search_field.setMinimumHeight(25)
        self.search_field.setMinimumWidth(180)
        self.search_field.addItems(["Title", "Author", "Publisher", "Genre Category"])
        self.search_field.setStyleSheet("font-size: 13px;")#padding: 5px; border: 0.5px solid;
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
        search_button.clicked.connect(self.search_books)
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
        add_button.clicked.connect(self.add_book)
        search_layout.addStretch()
        search_layout.addWidget(add_button)

        layout.addLayout(search_layout)

        # Book table
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setFont(QFont("Arial", 13))
        self.table.setRowHeight(0, 20)
        self.table.setShowGrid(True)
        self.table.setHorizontalHeaderLabels([
            "ID", "Title", "Author", "Publisher", "Genre", 
            "Publish Year", "Location", "Stock", "Status", "Actions"
        ])
        self.table.setStyleSheet("""
            border: 0.5px solid;
            font-size: 12px;
        """)
        # Set size policy to expand horizontally
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Allow manual resizing of columns
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        # Set initial column widths to distribute space
        self.table.horizontalHeader().setStretchLastSection(True)  # Ensure the last column stretches to fill remaining space
        # Set approximate initial widths for columns
        column_widths = [50, 220, 150, 150, 180, 150, 100, 80, 100, 60]  # Adjust these as needed
        for i, width in enumerate(column_widths):
            self.table.setColumnWidth(i, width)
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

        self.load_books()

    def load_books(self, books=None):
        if books is None:
            books = self.service.get_all_book_trans()
        
        self.table.setRowCount(len(books))
        for row, book in enumerate(books):
            self.table.setItem(row, 0, QTableWidgetItem(str(book.book_id)))
            self.table.setItem(row, 1, QTableWidgetItem(book.title))
            self.table.setItem(row, 2, QTableWidgetItem(book.author))
            self.table.setItem(row, 3, QTableWidgetItem(book.publisher or ""))
            self.table.setItem(row, 4, QTableWidgetItem(book.genre_category or ""))
            self.table.setItem(row, 5, QTableWidgetItem(str(book.publish_year) if book.publish_year else ""))
            self.table.setItem(row, 6, QTableWidgetItem(book.location or ""))
            stock_status = "Out of Stock" if book.is_out_of_stock else f"{book.qty_oh - book.qty_allocated}"
            self.table.setItem(row, 7, QTableWidgetItem(stock_status))
            display_status = "Displayed" if book.is_display else "Not Displayed"
            self.table.setItem(row, 8, QTableWidgetItem(display_status))

            # Action buttons (only Delete button)
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(5)
            action_widget.setStyleSheet("border: none;")

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
            delete_button.clicked.connect(lambda _, b=book.book_id: self.delete_book(b))
            action_layout.addWidget(delete_button)

            self.table.setCellWidget(row, 9, action_widget)

    def handle_double_click(self, index):
        row = index.row()
        book_id = int(self.table.item(row, 0).text())
        book = self.service.get_book_by_id(book_id)
        self.edit_book(book)

    def search_books(self):
        search_field = self.search_field.currentText().lower().replace(" ", "_")
        search_term = self.search_input.text().strip().lower()
        if not search_term:
            self.load_books()
            return

        books = self.service.get_all_book_trans()
        filtered_books = [
            book for book in books
            if search_term in str(getattr(book, search_field, "")).lower()
        ]
        self.load_books(filtered_books)

    def add_book(self):
        dialog = BookDialog(self, None, self.user_dto)
        if dialog.exec_():
            self.load_books()

    def edit_book(self, book):
        dialog = BookDialog(self, book, self.user_dto)
        if dialog.exec_():
            self.load_books()

    def delete_book(self, book_id):
        modal = ConfirmModal(self, message="Are you sure you want to delete this book?", title="Confirm Delete")
        if modal.exec_() == QtWidgets.QDialog.Accepted:
            if self.service.delete_book(book_id):
                self.load_books()
                show_success(parent=self.parent, message="Book deleted successfully!")
            else:
                show_error(parent=self.parent, message="Failed to delete book. It may be in use or does not exist.")