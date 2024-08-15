import sys
import logging
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QPushButton, QLineEdit, QLabel, QTextEdit, QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QRect
from checkbox_settings_logic import CheckboxSettingsLogic
from get_curr_shift import get_shift_info  # Імпортуємо нову функцію

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class CheckboxSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Налаштування Checkbox")
        self.setGeometry(0, 0, 600, 500)  # Збільшені розміри для додаткових елементів

        # Створення компонентів інтерфейсу
        layout = QVBoxLayout()

        # Форма для введення налаштувань
        self.settings_form = QFormLayout()

        # Поле для API URL
        self.api_url = QLineEdit("https://api.checkbox.ua")
        self.api_url.setFont(QFont("Arial", 10))
        self.settings_form.addRow(QLabel("API URL:"), self.api_url)

        # Поле для ключа ліцензії каси
        self.license_key = QLineEdit()
        self.license_key.setFont(QFont("Arial", 10))
        self.settings_form.addRow(QLabel("Ключ ліцензії каси:"), self.license_key)

        # Поле для логіну касира
        self.cashier_login = QLineEdit()
        self.cashier_login.setFont(QFont("Arial", 10))
        self.settings_form.addRow(QLabel("Логін касира:"), self.cashier_login)

        # Поле для пароля касира
        self.cashier_password = QLineEdit()
        self.cashier_password.setFont(QFont("Arial", 10))
        self.cashier_password.setEchoMode(QLineEdit.Password)  # Приховувати пароль
        self.settings_form.addRow(QLabel("Пароль касира:"), self.cashier_password)

        layout.addLayout(self.settings_form)

        # Кнопка "Авторизуватись"
        self.authenticate_button = QPushButton("Авторизуватись")
        self.authenticate_button.setFont(QFont("Arial", 10))
        self.authenticate_button.setFixedSize(150, 30)
        self.authenticate_button.clicked.connect(self.authenticate)
        layout.addWidget(self.authenticate_button)

        # Кнопка "Отримати зміну"
        self.get_shift_button = QPushButton("Отримати зміну")
        self.get_shift_button.setFont(QFont("Arial", 10))
        self.get_shift_button.setFixedSize(150, 30)
        self.get_shift_button.clicked.connect(self.handle_get_shift_info)
        layout.addWidget(self.get_shift_button)

        # Текстовий блок для інформації про зміну
        self.info_text = QTextEdit()
        self.info_text.setFont(QFont("Arial", 10))
        self.info_text.setReadOnly(True)
        layout.addWidget(self.info_text)

        self.setLayout(layout)

        # Центрування вікна відносно батьківського вікна
        if parent:
            self.setGeometry(self.center_on_parent(parent))

        # Створення об'єкта бізнес-логіки
        self.logic = CheckboxSettingsLogic(self)

        # Завантаження налаштувань з бази даних
        self.logic.load_settings_from_db()

    def authenticate(self):
        """Виклик функції авторизації з логіки"""
        self.logic.authenticate()

    def handle_get_shift_info(self):
        """Обробка натискання кнопки 'Отримати зміну'"""
        api_url = self.api_url.text()
        access_token = self.logic.access_token
        if not access_token:
            self.info_text.setHtml("<font color='red'>Токен доступу відсутній. Спочатку авторизуйтесь.</font>")
            return

        # Виклик функції з `get_curr_shift.py`
        get_shift_info(api_url, access_token, self.info_text)

    def center_on_parent(self, parent):
        """Центрує вікно на батьківському вікні."""
        parent_rect = parent.geometry()
        dialog_rect = self.geometry()

        x = parent_rect.left() + (parent_rect.width() - dialog_rect.width()) / 2
        y = parent_rect.top() + (parent_rect.height() - dialog_rect.height()) / 2

        return QRect(int(x), int(y), dialog_rect.width(), dialog_rect.height())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    parent_window = QDialog()
    parent_window.setWindowTitle("Батьківське вікно")
    parent_window.setGeometry(100, 100, 800, 600)
    parent_window.show()

    dialog = CheckboxSettingsDialog(parent=parent_window)
    dialog.exec_()
