from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction, QVBoxLayout, QWidget, QTableWidget, QHeaderView, \
    QSizePolicy, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
import sys
import os
from .license_dialog import LicenseDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Inventory Management System")
        self.setGeometry(100, 100, 1024, 768)

        # Створення головного віджета
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # Створення лейаута
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        # Додавання панелі інструментів
        self.create_toolbar()

        # Додавання таблиці для відображення даних
        self.table = QTableWidget()
        self.table.setRowCount(10)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['Замовлення', 'ТТН', 'ПІБ Клієнта', 'Статус', 'Отримано', 'Фіскалізовано'])

        # Налаштування автоматичного растяження колонок
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.layout.addWidget(self.table)

    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(70, 70))
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        toolbar.setMovable(False)
        toolbar.setFloatable(False)

        self.addToolBar(Qt.TopToolBarArea, toolbar)

        icon_path = os.path.join(os.path.dirname(__file__), '..', 'ico')

        add_order_action = QAction(QIcon(os.path.join(icon_path, 'Nova.png')), "Додати замовлення", self)
        add_order_action.setStatusTip("Додати нове замовлення")
        add_order_action.triggered.connect(self.add_order)
        toolbar.addAction(add_order_action)

        update_status_action = QAction(QIcon(os.path.join(icon_path, 'refresh.png')), "Оновити статус", self)
        update_status_action.setStatusTip("Оновити статус замовлення")
        update_status_action.triggered.connect(self.update_status)
        toolbar.addAction(update_status_action)

        spacer_widget = QWidget()
        spacer_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer_widget)

        update_key_action = QAction(QIcon(os.path.join(icon_path, 'key.webp')), "Оновити ключ", self)
        update_key_action.setStatusTip("Оновити ключ")
        update_key_action.triggered.connect(self.update_key)
        toolbar.addAction(update_key_action)

    def add_order(self):
        print("Додати замовлення")

    def update_status(self):
        print("Оновити статус")

    def update_key(self):
        dialog = LicenseDialog()
        dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
