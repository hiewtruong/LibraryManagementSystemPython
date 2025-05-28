from PyQt5.QtWidgets import QWidget
from lib.common_ui.notification_modal import ErrorModal,SuccessModal,WarningModal

def show_error(parent: QWidget, message: str):
    if parent is not None:
        modal = ErrorModal(parent, message)
        modal.exec_()

def show_success(parent: QWidget, message: str):
    if parent is not None:
        modal = SuccessModal(parent, message)
        modal.exec_()

def show_warning(parent: QWidget, message: str):
    if parent is not None:
        modal = WarningModal(parent, message)
        modal.exec_()