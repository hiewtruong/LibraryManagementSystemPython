from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QComboBox, QHeaderView, QSizePolicy, QMessageBox, QDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from services.author.author_service import AuthorService
from domain.entities.author import Author
from lib.common_ui.confirm_modal import ConfirmModal

class AuthorPanel(QWidget):
    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: white;")
        self.parent = parent
        self.user = user
        self.service = AuthorService.get_instance()
        self.init_ui()
        self.setMinimumSize(1370, 830)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 10, 10, 10)
        layout.setSpacing(5)

        # Title
        title_label = QLabel("Manage Authors")
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
        search_label.setStyleSheet("border: none;")
        search_label.setMaximumWidth(50)
        search_layout.addWidget(search_label)

        # Search components
        self.search_field = QComboBox()
        self.search_field.setMaximumWidth(180)
        self.search_field.setMinimumHeight(25)
        self.search_field.setMinimumWidth(150)
        self.search_field.addItems(["Author Name", "Created By", "Update By"])
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
        search_button.clicked.connect(self.search_authors)
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
        add_button.clicked.connect(self.add_author)
        search_layout.addStretch()
        search_layout.addWidget(add_button)

        layout.addLayout(search_layout)

        # Author table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setFont(QFont("Arial", 13))
        self.table.setRowHeight(0, 20)
        self.table.setShowGrid(True)
        self.table.setHorizontalHeaderLabels([
            "AuthorID", "AuthorName", "IsDeleted", "CreatedDt", "CreatedBy", "UpdateDt", "UpdateBy", "Actions"
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

        self.load_authors()

    def load_authors(self, authors=None):
        if authors is None:
            authors = self.service.get_all_authors()

        self.table.setRowCount(len(authors))
        for row, author in enumerate(authors):
            self.table.setItem(row, 0, QTableWidgetItem(str(author.author_id)))
            self.table.setItem(row, 1, QTableWidgetItem(author.author_name))
            self.table.setItem(row, 2, QTableWidgetItem(str(author.is_deleted)))
            self.table.setItem(row, 3, QTableWidgetItem(str(author.created_dt)))
            self.table.setItem(row, 4, QTableWidgetItem(author.created_by))
            self.table.setItem(row, 5, QTableWidgetItem(str(author.update_dt)))
            self.table.setItem(row, 6, QTableWidgetItem(author.update_by))

            # Action buttons (only Delete button)
            action_widget = QWidget()
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
            delete_button.clicked.connect(lambda _, a_id=author.author_id: self.delete_author(a_id))
            action_layout.addWidget(delete_button)

            self.table.setCellWidget(row, 7, action_widget)

    def handle_double_click(self, index):
        row = index.row()
        author_id = int(self.table.item(row, 0).text())
        author = self.service.get_author_by_id(author_id)
        self.edit_author(author)

    def search_authors(self):
        search_field = self.search_field.currentText().lower().replace(" ", "_")
        search_term = self.search_input.text().strip().lower()
        if not search_term:
            self.load_authors()
            return

        authors = self.service.get_all_authors()
        filtered_authors = [
            author for author in authors
            if search_term in str(getattr(author, search_field, "")).lower()
        ]
        self.load_authors(filtered_authors)

    def add_author(self):
        from views.author.create_author_modal import CreateAuthorModal
        from lib.common_ui.confirm_modal import ConfirmModal
        dialog = CreateAuthorModal(controller=self.service, parent=self)
        if dialog.exec_():
            confirm = ConfirmModal(self, message="Do you want to add this author?", title="Confirm Add")
            if confirm.exec_() == QDialog.Accepted:
                self.load_authors()

    def edit_author(self, author):
        from views.author.create_author_modal import CreateAuthorModal
        from lib.common_ui.confirm_modal import ConfirmModal
        dialog = CreateAuthorModal(controller=self.service, author=author, parent=self)
        if dialog.exec_():
            confirm = ConfirmModal(self, message="Do you want to update this author?", title="Confirm Update")
            if confirm.exec_() == QDialog.Accepted:
                self.load_authors()

    def delete_author(self, author_id):
        from lib.common_ui.confirm_modal import ConfirmModal
        confirm = ConfirmModal(self, message="Are you sure you want to delete this author?", title="Confirm Delete")
        if confirm.exec_() == QDialog.Accepted:
            if self.service.delete_author(author_id):
                self.load_authors()
