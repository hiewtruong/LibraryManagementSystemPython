from PyQt5 import QtCore, QtGui, QtWidgets
from domain.dto.user.user_login_dto import UserLoginDTO
from views.book.book_panel import BookPanel
from views.author.author_panel import AuthorPanel
from views.category.category_panel import CategoryPanel
from views.transactions_loan.create_transaction_loan_panel import CreateTransactionLoanPanel
from views.transactions_loan.transaction_loan_panel import TransactionLoanPanel
from views.user.user_panel import UserPanel
from lib.common_ui.confirm_modal import ConfirmModal
from controllers.transaction_loan_controller import TransactionLoanController

class Ui_AdminDashboard(QtWidgets.QMainWindow):
    def __init__(self, user_dto):
        super().__init__()
        self.user_dto = user_dto
        self.setupUi(self)
        self._center_window(1600, 900)
        self.setFixedSize(1600, 900)
        self.current_panel = None
        self.controller = None
        self._connect_signals()

    def setupUi(self, MainWindow):
        user_dto = self.user_dto
        self.ui = Ui_Form()
        self.ui.setupUi(MainWindow)

        MainWindow.setStyleSheet("background-color: white;")

        self.ui.pushButton.setText("Manage Books")
        self.ui.pushButton_2.setText("Manage Authors")
        self.ui.pushButton_3.setText("Manage Categories")
        self.ui.pushButton_4.setText("Manage Users")
        self.ui.pushButton_5.setText("Manage Loan Transactions")
        self.ui.pushButton_7.setText("Create Transaction")
        self.ui.pushButton_6.setText("Exit")
        self.ui.pushButton_6.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)

        if hasattr(user_dto, 'user_name') and hasattr(user_dto, 'role_name'):
            self.ui.label_2.setText(f"{user_dto.user_name} / {user_dto.role_name}")
        else:
            self.ui.label_2.setText("Not Identified / Not Identified")

        self.ui.label_3.setText("Welcome to Library Management System")

    def _center_window(self, width, height):
        screen = self.screen().availableGeometry()
        screen_width = screen.width()
        screen_height = screen.height()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.setGeometry(x, y, width, height)

    def _connect_signals(self):
        self.ui.pushButton.clicked.connect(self.show_book_panel)
        self.ui.pushButton_2.clicked.connect(self.show_author_panel)
        self.ui.pushButton_3.clicked.connect(self.show_category_panel)
        self.ui.pushButton_4.clicked.connect(self.show_user_panel)
        self.ui.pushButton_5.clicked.connect(self.show_transaction_loan_panel)
        self.ui.pushButton_7.clicked.connect(self.show_create_transaction_loan_panel)
        self.ui.pushButton_6.clicked.connect(self._confirm_exit)

    def clear_content(self):
        if self.current_panel is not None:
            self.current_panel.setParent(None)
            self.current_panel.deleteLater()
            self.current_panel = None

        if hasattr(self.ui, 'label_3') and self.ui.label_3 is not None and self.ui.label_3.isVisible():
            self.ui.label_3.hide()

        if hasattr(self.ui, 'label_3') and self.ui.label_3 is not None and self.ui.label_3.parent() is not None:
            self.ui.label_3.hide()

    def show_book_panel(self):
        self.clear_content()
        self.current_panel = BookPanel(self.ui.frame_3)
        self.current_panel.setObjectName("content_panel")
        self.current_panel.controller = self.controller 
        self.current_panel.show()
        if hasattr(self.current_panel, 'load_data'):
            self.current_panel.load_data()

    def show_author_panel(self):
        self.clear_content()
        self.current_panel = AuthorPanel(self.ui.frame_3)
        self.current_panel.setObjectName("content_panel")
        self.current_panel.controller = self.controller
        self.current_panel.show()
        if hasattr(self.current_panel, 'load_data'):
            self.current_panel.load_data()

    def show_category_panel(self):
        self.clear_content()
        self.current_panel = CategoryPanel(self.ui.frame_3)
        self.current_panel.setObjectName("content_panel")
        self.current_panel.controller = self.controller
        self.current_panel.show()
        if hasattr(self.current_panel, 'load_data'):
            self.current_panel.load_data()

    def show_user_panel(self):
        self.clear_content()
        self.current_panel = UserPanel(self.ui.frame_3)
        self.current_panel.setObjectName("content_panel")
        self.current_panel.controller = self.controller 
        self.current_panel.show()
        if hasattr(self.current_panel, 'load_data'):
            self.current_panel.load_data()

    def show_transaction_loan_panel(self):
        self.clear_content()
        self.current_panel = TransactionLoanPanel(self.ui.frame_3)
        self.current_panel.setObjectName("content_panel")
        self.current_panel.controller = TransactionLoanController(self)
        self.current_panel.show()
        self.current_panel.load_data() 

    def show_create_transaction_loan_panel(self):
        self.clear_content()
        self.current_panel = CreateTransactionLoanPanel(self.ui.frame_3)
        self.current_panel.setObjectName("content_panel")
        self.current_panel.controller = TransactionLoanController(self) 
        self.current_panel.show()
        self.current_panel.load_data() 

    def _confirm_exit(self):
        modal = ConfirmModal(self, message="Are you sure you want to exit?", title="Confirm Exit")
        if modal.exec_() == QtWidgets.QDialog.Accepted:
            self.close()

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1600, 900)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(10, 10, 191, 881))
        self.frame.setStyleSheet("QFrame { background-color: white; border: 2px solid black; border-radius: 5px; }")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(20, 120, 151, 31))
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 170, 151, 31))
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 220, 151, 31))
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QtWidgets.QPushButton(self.frame)
        self.pushButton_4.setGeometry(QtCore.QRect(20, 270, 151, 31))
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_5 = QtWidgets.QPushButton(self.frame)
        self.pushButton_5.setGeometry(QtCore.QRect(20, 320, 151, 31))
        self.pushButton_5.setObjectName("pushButton_5")

        self.pushButton_7 = QtWidgets.QPushButton(self.frame)
        self.pushButton_7.setGeometry(QtCore.QRect(20, 370, 151, 31))
        self.pushButton_7.setObjectName("pushButton_7")

        self.pushButton_6 = QtWidgets.QPushButton(self.frame)
        self.pushButton_6.setGeometry(QtCore.QRect(20, 840, 151, 31))
        self.pushButton_6.setObjectName("pushButton_6")

        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(40, 30, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setGeometry(QtCore.QRect(210, 10, 1241, 31))
        self.frame_2.setStyleSheet("QFrame { background-color: white; border: 2px solid black; border-radius: 5px; }")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        self.frame_3 = QtWidgets.QFrame(Form)
        self.frame_3.setGeometry(QtCore.QRect(210, 50, 1381, 841))
        self.frame_3.setStyleSheet("QFrame { background-color: white; border: 2px solid black; border-radius: 5px; }")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")

        self.label_3 = QtWidgets.QLabel(self.frame_3)
        self.label_3.setGeometry(QtCore.QRect(350, 340, 681, 81))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")

        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(1460, 20, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("QLabel { border: none; }")
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Manage Books"))
        self.pushButton_2.setText(_translate("Form", "Manage Authors"))
        self.pushButton_3.setText(_translate("Form", "Manage Categories"))
        self.pushButton_4.setText(_translate("Form", "Manage Users"))
        self.pushButton_5.setText(_translate("Form", "Manage Loan Transactions"))
        self.pushButton_7.setText(_translate("Form", "Create Transaction"))
        self.pushButton_6.setText(_translate("Form", "Exit"))
        self.label.setText(_translate("Form", "MENU"))
        self.label_3.setText(_translate("Form", "Welcome to Library Management System"))