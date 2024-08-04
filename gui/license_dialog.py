from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox, QComboBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication, Qt
import pyperclip
from license_manager import get_device_id, verify_license_key, save_license, get_license
from datetime import datetime, timedelta


class LicenseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Оновлення ключа')
        self.setGeometry(100, 100, 400, 250)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)  # Зменшити відступи між краями діалогу і макетом
        layout.setSpacing(2)  # Зменшити вертикальні відступи між елементами

        device_id = get_device_id()
        device_id_label = QLabel(f'DEVICE_ID: {device_id}')

        copy_button = QPushButton('Скопіювати DEVICE_ID')
        copy_button.clicked.connect(lambda: self.copy_device_id(device_id))

        # Групування device_id_label і copy_button на одному рівні
        device_layout = QHBoxLayout()
        device_layout.setContentsMargins(0, 0, 0, 0)  # Зменшити відступи між елементами в групі
        device_layout.addWidget(device_id_label)
        device_layout.addWidget(copy_button)
        layout.addLayout(device_layout)

        # Отримати інформацію про існуючу ліцензію
        license_info = get_license(device_id)
        if license_info:
            expiry_date = datetime.strptime(license_info[4], '%Y-%m-%d')
            if datetime.now() < expiry_date:
                license_status_label = QLabel(f'Ліцензія діє до: {expiry_date.strftime("%Y-%m-%d")}')
                license_status_label.setStyleSheet('color: green;')
            else:
                license_status_label = QLabel(f'Ліцензія прострочена: {expiry_date.strftime("%Y-%м-%д")}')
                license_status_label.setStyleSheet('color: red;')
        else:
            license_status_label = QLabel('Ліцензія відсутня')

        layout.addWidget(license_status_label)

        font = QFont()
        font.setPointSize(14)  # Зменшує розмір шрифту для поля вводу та випадаючого списку

        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText('Введіть ліцензійний ключ')
        self.key_input.setFont(font)
        self.key_input.setFixedHeight(30)  # Встановлює фіксовану висоту
        layout.addWidget(self.key_input)

        # Додавання випадаючого списку
        months_layout = QHBoxLayout()
        months_layout.setContentsMargins(0, 0, 0, 0)  # Зменшити відступи між елементами в групі
        months_label = QLabel('Кількість місяців:')
        self.months_combo = QComboBox()
        self.months_combo.addItems([str(i) for i in range(1, 13)])
        self.months_combo.setFont(font)  # Налаштування шрифту для випадаючого списку
        self.months_combo.setFixedHeight(30)  # Встановлює фіксовану висоту

        months_layout.addWidget(months_label)
        months_layout.addWidget(self.months_combo)
        layout.addLayout(months_layout)

        # Створення горизонтального макету для кнопок
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)  # Зменшити відступи між елементами в групі
        button_font = QFont()
        button_font.setPointSize(14)  # Розмір шрифту для кнопок
        button_height = 30  # Висота кнопок

        confirm_button = QPushButton('Підтвердити')
        confirm_button.setFont(button_font)
        confirm_button.setFixedHeight(button_height)
        confirm_button.clicked.connect(self.confirm_key)

        cancel_button = QPushButton('Відхилити')
        cancel_button.setFont(button_font)
        cancel_button.setFixedHeight(button_height)
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
        months = int(self.months_combo.currentText())
        if verify_license_key(device_id, license_key, months):
            save_license(device_id, license_key, datetime.now() + timedelta(days=30 * months))
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
