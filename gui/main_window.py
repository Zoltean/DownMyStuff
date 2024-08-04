from PyQt5.QtWidgets import QMainWindow, QApplication, QToolBar, QAction, QVBoxLayout, QWidget, QTableWidget, \
    QHeaderView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Inventory Management System")
        self.setGeometry(100, 100, 1024, 768)  # Це можна залишити, але воно буде перекрите showMaximized()

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

        # Налаштування автоматического растяження колонок
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.layout.addWidget(self.table)

    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(70, 70))
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        toolbar.setMovable(False)
        toolbar.setFloatable(False)

        self.addToolBar(Qt.TopToolBarArea, toolbar)  # Установка тулбара сверху

        # Додавання кнопок на панель інструментів
        add_order_action = QAction(QIcon(r"C:\Users\toxik\Downloads\images.png"), "Додати замовлення", self)
        add_order_action.setStatusTip("Додати нове замовлення")
        add_order_action.triggered.connect(self.add_order)
        toolbar.addAction(add_order_action)

        update_status_action = QAction(QIcon(r"C:\Users\toxik\Downloads\free-refresh-icon-3104-thumb.png"),
                                       "Оновити статус", self)
        update_status_action.setStatusTip("Оновити статус замовлення")
        update_status_action.triggered.connect(self.update_status)
        toolbar.addAction(update_status_action)

    def add_order(self):
        # Логіка для додавання замовлення
        print("Додати замовлення")

    def update_status(self):
        # Логіка для оновлення статусу
        print("Оновити статус")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()  # Відкриває вікно на весь екран
    sys.exit(app.exec_())
