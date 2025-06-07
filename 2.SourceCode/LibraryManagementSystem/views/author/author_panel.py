from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt

class AuthorPanel(QWidget):
    def __init__(self, controller=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        print(f"[AuthorPanel] Initialized with controller type: {type(self.controller)}")
        self.initUI()
        self.setMinimumSize(1370, 830)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

    def initUI(self):
        self.setWindowTitle("Manage Authors")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 10, 10)
        main_layout.setSpacing(10)

        # Title label
        title_label = QLabel("Manage Authors")
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
        self.search_field.addItems(["Author Name", "Created By", "Update By"])
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
        search_button.clicked.connect(self.search_authors)
        search_layout.addWidget(search_button)

        # Add New button (reposition to right with stretch)
        search_layout.addStretch()
        add_button = QPushButton("Add New")
        add_button.setFixedHeight(25)
        add_button.setStyleSheet("""
            background-color: #2196F3;
            color: white;
            border-radius: 5px;
        """)
        add_button.clicked.connect(self.create_new_author)
        search_layout.addWidget(add_button)

        main_layout.addLayout(search_layout)

        # Author table
        self.author_table = QTableWidget()
        self.author_table.setColumnCount(9)
        self.author_table.setHorizontalHeaderLabels([
            "AuthorID", "AuthorName", "IsDeleted", "CreatedDt", "CreatedBy", "UpdateDt", "UpdateBy", "Edit", "Delete"
        ])
        self.author_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.author_table.horizontalHeader().setStretchLastSection(True)
        self.author_table.verticalHeader().setVisible(False)
        self.author_table.setAlternatingRowColors(True)
        self.author_table.setStyleSheet("""
            alternate-background-color: #f9f9f9;
            background-color: white;
            border: 0.5px solid;
        """)
        self.author_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.author_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.author_table.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        main_layout.addWidget(self.author_table)

        # Bottom panel with total label (keep as is)
        bottom_panel = QHBoxLayout()
        bottom_panel.addStretch()
        self.total_label = QLabel("Total: 0")
        bottom_panel.addWidget(self.total_label)
        main_layout.addLayout(bottom_panel)

        # Load all authors on init
        if self.controller:
            authors = self.controller.get_all_authors()
            self.load_author_data(authors)

    def load_author_data(self, authors):
        self.author_table.setRowCount(len(authors))
        for row, author in enumerate(authors):
            self.author_table.setItem(row, 0, QTableWidgetItem(str(getattr(author, 'author_id', ''))))
            self.author_table.setItem(row, 1, QTableWidgetItem(getattr(author, 'author_name', '')))
            self.author_table.setItem(row, 2, QTableWidgetItem(str(getattr(author, 'is_deleted', ''))))
            self.author_table.setItem(row, 3, QTableWidgetItem(str(getattr(author, 'created_dt', ''))))
            self.author_table.setItem(row, 4, QTableWidgetItem(getattr(author, 'created_by', '')))
            self.author_table.setItem(row, 5, QTableWidgetItem(str(getattr(author, 'update_dt', ''))))
            self.author_table.setItem(row, 6, QTableWidgetItem(getattr(author, 'update_by', '')))

            # Action buttons
            action_widget_edit = QPushButton("Edit")
            action_widget_edit.setStyleSheet("""
                padding: 3px 10px;
                font-size: 12px;
                background-color: #FFC107;
                color: white;
                border: none;
                border-radius: 3px;
            """)
            action_widget_edit.clicked.connect(lambda _, a=author: self.edit_author(a))

            action_widget_delete = QPushButton("Delete")
            action_widget_delete.setStyleSheet("""
                padding: 3px 10px;
                font-size: 12px;
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 3px;
            """)
            action_widget_delete.clicked.connect(lambda _, a_id=author.author_id: self.delete_author(a_id))

            self.author_table.setCellWidget(row, 7, action_widget_edit)
            self.author_table.setCellWidget(row, 8, action_widget_delete)

        self.total_label.setText(f"Total: {len(authors)}")

    def search_authors(self):
        search_field = self.search_field.currentText().lower().replace(" ", "_")
        search_term = self.search_input.text().strip().lower()
        if not search_term:
            if self.controller:
                authors = self.controller.get_all_authors()
                self.load_author_data(authors)
            return

        if self.controller:
            authors = self.controller.get_all_authors()
            filtered_authors = [
                author for author in authors
                if search_term in str(getattr(author, search_field, "")).lower()
            ]
            self.load_author_data(filtered_authors)
        else:
            QMessageBox.warning(self, "Warning", "Controller not set.")

    def create_new_author(self):
        if self.controller:
            from views.author.create_author_modal import CreateAuthorModal
            dialog = CreateAuthorModal(controller=self.controller, parent=self)
            if dialog.exec_():
                authors = self.controller.get_all_authors()
                self.load_author_data(authors)
                # Notify controller about success
                if hasattr(self.controller, 'notify_author_added'):
                    self.controller.notify_author_added()
        else:
            # Notify controller about missing controller
            if hasattr(self.controller, 'notify_controller_missing'):
                self.controller.notify_controller_missing()

    def edit_author(self, author):
        if self.controller:
            from views.author.create_author_modal import CreateAuthorModal
            dialog = CreateAuthorModal(controller=self.controller, author=author, parent=self)
            if dialog.exec_():
                authors = self.controller.get_all_authors()
                self.load_author_data(authors)
                # Notify controller about success
                if hasattr(self.controller, 'notify_author_updated'):
                    self.controller.notify_author_updated()
        else:
            if hasattr(self.controller, 'notify_controller_missing'):
                self.controller.notify_controller_missing()

    def delete_author(self, author_id):
        # Notify controller to confirm deletion
        if self.controller and hasattr(self.controller, 'confirm_author_deletion'):
            confirmed = self.controller.confirm_author_deletion(author_id)
            if confirmed:
                if self.controller.delete_author(author_id):
                    authors = self.controller.get_all_authors()
                    self.load_author_data(authors)
