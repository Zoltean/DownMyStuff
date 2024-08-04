from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QMessageBox
from user_management.auth import AuthService
from user_management.user_service import UserService


class UserManagement(QMainWindow):
    def __init__(self, user_service):
        super().__init__()
        self.user_service = user_service
        self.setWindowTitle("User Management")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.add_user_button = QPushButton("Add User")

        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.add_user_button)

        self.add_user_button.clicked.connect(self.add_user)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def add_user(self):
        username = self.username_input.text()
        password = AuthService.hash_password(self.password_input.text())
        try:
            self.user_service.add_user(username, password)
            QMessageBox.information(self, "Success", "User added successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
