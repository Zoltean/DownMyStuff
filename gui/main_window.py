import os
import sys
from datetime import datetime
from PyQt5.QtCore import Qt, QSize, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction, QVBoxLayout, QWidget, QTableWidget, QHeaderView, \
    QSizePolicy, QApplication, QLabel
from license_manager import get_device_id, get_license
from .license_dialog import LicenseDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Inventory Management System")
        self.setGeometry(100, 100, 1024, 768)
        self.center()  # Центрує основне вікно

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        self.license_info_label = QLabel("Строк дії ліцензії: Перевірка...")
        self.layout.addWidget(self.license_info_label)

        self.create_toolbar()

        self.table = QTableWidget()
        self.table.setRowCount(10)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['Замовлення', 'ТТН', 'ПІБ Клієнта', 'Статус', 'Отримано', 'Фіскалізовано'])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.layout.addWidget(self.table)

        self.update_license_info()

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
        dialog = LicenseDialog(self)
        dialog.exec_()
        self.update_license_info()

    def update_license_info(self):
        """Оновлює інформацію про строк дії ліцензії."""
        device_id = get_device_id()
        license_info = get_license(device_id)

        today = datetime.now()
        if license_info:
            try:
                expiration_date = datetime.strptime(license_info[4], '%Y-%m-%d')
                days_remaining = (expiration_date - today).days

                if today < expiration_date:
                    if days_remaining > 10:
                        color = 'green'
                    else:
                        color = 'yellow'
                    self.license_info_label.setText(
                        f'<span style="color:{color}">Строк дії ліцензії: до {expiration_date.strftime("%Y-%m-%d")}</span>')
                else:
                    self.license_info_label.setText('<span style="color:red">Строк дії ліцензії закінчився</span>')
            except ValueError:
                self.license_info_label.setText('<span style="color:red">Помилка формату дати ліцензії</span>')
        else:
            self.license_info_label.setText('<span style="color:red">Ліцензія не знайдена</span>')

    def center(self):
        # Отримати розміри екрану
        screen_rect = QCoreApplication.instance().primaryScreen().geometry()
        # Розміри основного вікна
        window_rect = self.geometry()
        x = (screen_rect.width() - window_rect.width()) / 2
        y = (screen_rect.height() - window_rect.height()) / 2
        self.move(int(x), int(y))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
