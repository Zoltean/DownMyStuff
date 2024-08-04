from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from user_management.auth import AuthService
from user_management.user_service import UserService


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory Management System")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        self.product_management_button = QPushButton("Manage Products")
        self.statistics_button = QPushButton("View Statistics")
        self.user_management_button = QPushButton("User Management")

        self.layout.addWidget(self.product_management_button)
        self.layout.addWidget(self.statistics_button)
        self.layout.addWidget(self.user_management_button)

        self.product_service = ProductService('products.db')
        self.user_service = UserService('users.db')

        self.product_management_button.clicked.connect(self.open_product_management)
        self.statistics_button.clicked.connect(self.open_statistics)
        self.user_management_button.clicked.connect(self.open_user_management)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def open_product_management(self):
        self.product_management = ProductManagement(self.product_service)
        self.product_management.show()

    def open_statistics(self):
        self.statistics_view = StatisticsView(self.product_service)
        self.statistics_view.show()

    def open_user_management(self):
        self.user_management = UserManagement(self.user_service)
        self.user_management.show()
