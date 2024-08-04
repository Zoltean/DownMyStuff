from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QFont
import pyperclip
from license_manager import get_device_id, verify_license_key, save_license
from datetime import datetime, timedelta
from PyQt5.QtCore import QCoreApplication, Qt, QRect

class LicenseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Оновлення ключа')
        self.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout()

        device_id = get_device_id()
        device_id_label = QLabel(f'DEVICE_ID: {device_id}')
        layout.addWidget(device_id_label)

        copy_button = QPushButton('Скопіювати DEVICE_ID')
        copy_button.clicked.connect(lambda: self.copy_device_id(device_id))
        layout.addWidget(copy_button)

        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText('Введіть ліцензійний ключ')

        # Налаштування шрифту
        font = QFont()
        font.setPointSize(16)  # Збільшує розмір шрифту
        self.key_input.setFont(font)

        # Налаштування висоти
        self.key_input.setFixedHeight(50)  # Встановлює фіксовану висоту

        layout.addWidget(self.key_input)

        # Створення горизонтального макету для кнопок
        buttons_layout = QHBoxLayout()
        confirm_button = QPushButton('Підтвердити')
        confirm_button.clicked.connect(self.confirm_key)
        cancel_button = QPushButton('Відхилити')
        cancel_button.clicked.connect(self.close)

        buttons_layout.addWidget(confirm_button)
        buttons_layout.addStretch()  # Додає простір між кнопками
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def copy_device_id(self, device_id):
        pyperclip.copy(device_id)
        QMessageBox.information(self, 'Копіювання', 'Ваш DEVICE_ID зкопійовано до буферу', QMessageBox.Ok)

    def confirm_key(self):
        device_id = get_device_id()
        license_key = self.key_input.text()
        if verify_license_key(device_id, license_key):
            save_license(device_id, license_key, datetime.now() + timedelta(days=60))  # Наприклад, 2 місяці
            QMessageBox.information(self, 'Успіх', 'Ліцензійний ключ успішно активовано!', QMessageBox.Ok)
            self.accept()  # Закриває діалогове вікно і повертає результат
        else:
            QMessageBox.critical(self, 'Помилка', 'Невірний ліцензійний ключ!', QMessageBox.Ok)

    def showEvent(self, event):
        super().showEvent(event)
        self.center()

    def center(self):
        # Отримати розміри екрану
        screen_rect = QCoreApplication.instance().primaryScreen().geometry()
        # Розміри діалогового вікна
        dialog_rect = self.geometry()
        # Вирахувати координати для центрування
        x = (screen_rect.width() - dialog_rect.width()) / 2
        y = (screen_rect.height() - dialog_rect.height()) / 2
        self.move(int(x), int(y))
