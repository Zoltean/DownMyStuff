import sys
import sqlite3
import requests
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QPushButton, QLineEdit, QLabel, QApplication, QMessageBox, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QRect

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

        # Текстовий блок для інформації про касира та податкові ставки
        self.info_text = QTextEdit()
        self.info_text.setFont(QFont("Arial", 10))
        self.info_text.setReadOnly(True)
        layout.addWidget(self.info_text)

        self.setLayout(layout)

        # Центрування вікна відносно батьківського вікна
        if parent:
            self.setGeometry(self.center_on_parent(parent))

        # Завантаження налаштувань з бази даних
        self.load_settings_from_db()

    def load_settings_from_db(self):
        """Завантажує налаштування з бази даних і заповнює поля форми."""
        try:
            # Підключення до бази даних
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            # Отримання останнього запису
            cursor.execute('SELECT license_key, cashier_login, cashier_password, access_token FROM checkbox_settings ORDER BY id DESC LIMIT 1')
            row = cursor.fetchone()

            if row:
                license_key, cashier_login, cashier_password, access_token = row
                self.license_key.setText(license_key)
                self.cashier_login.setText(cashier_login)
                self.cashier_password.setText(cashier_password)

                # Отримання інформації про касира та податкові ставки
                self.get_cashier_info(access_token)
                self.get_taxes_info(access_token)

            conn.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зчитати налаштування з бази даних: {e}")

    def authenticate(self):
        # Логіка для авторизації
        api_url = self.api_url.text()
        license_key = self.license_key.text()
        login = self.cashier_login.text()
        password = self.cashier_password.text()

        headers = {
            'accept': 'application/json',
            'X-Client-Name': 'Test-Client-Name',
            'X-Client-Version': 'Test-Client-Version',
            'Content-Type': 'application/json'
        }

        payload = {
            "login": login,
            "password": password
        }

        try:
            response = requests.post(f"{api_url}/api/v1/cashier/signin", json=payload, headers=headers)
            response.raise_for_status()  # Перевірка наявності помилок HTTP

            response_data = response.json()
            access_token = response_data.get('access_token')

            if response.status_code == 200:
                QMessageBox.information(self, "Авторизація успішна", f"Токен доступу: {access_token}")
                self.save_settings_to_db(license_key, login, password, access_token)
                # Отримання інформації про касира та податкові ставки
                self.get_cashier_info(access_token)
                self.get_taxes_info(access_token)
            else:
                QMessageBox.warning(self, "Помилка авторизації", f"Помилка: {response.text}")

        except requests.RequestException as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося здійснити запит: {e}")

    def save_settings_to_db(self, license_key, login, password, access_token):
        """Зберігає налаштування у базі даних"""
        try:
            # Підключення до бази даних
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            # Створення таблиці, якщо не існує
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS checkbox_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    license_key TEXT,
                    cashier_login TEXT,
                    cashier_password TEXT,
                    access_token TEXT
                )
            ''')

            # Вставка даних у таблицю checkbox_settings
            cursor.execute('''
                INSERT INTO checkbox_settings (license_key, cashier_login, cashier_password, access_token)
                VALUES (?, ?, ?, ?)
            ''', (license_key, login, password, access_token))

            conn.commit()
            conn.close()

            QMessageBox.information(self, "Успішно", "Налаштування збережено в базі даних.")

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти налаштування в базі даних: {e}")

    def get_cashier_info(self, access_token):
        """Отримує інформацію про касира і оновлює текстовий блок"""
        api_url = self.api_url.text()

        headers = {
            'accept': 'application/json',
            'X-Client-Name': 'Test-Client-Name',
            'X-Client-Version': 'Test-Client-Version',
            'Authorization': f'Bearer {access_token}'
        }

        try:
            response = requests.get(f"{api_url}/api/v1/cashier/me", headers=headers)
            response.raise_for_status()  # Перевірка наявності помилок HTTP

            cashier_data = response.json()

            # Форматування даних для відображення
            organization = cashier_data.get('organization', {})
            info = (
                f"<b>Назва організації:</b> <font color='green'><b>{organization.get('title', 'N/A')}</b></font><br>"
                f"<b>ЕДРПОУ:</b> <font color='green'><b>{organization.get('edrpou', 'N/A')}</b></font><br>"
                f"<b>Податкові ставки:</b> <font color='green'><b>{organization.get('tax_number', 'N/A')}</b></font><br>"
                f"<b>Ім'я касира:</b> <font color='green'><b>{cashier_data.get('full_name', 'N/A')}</b></font><br>"
                f"<b>Срок дії ключа:</b> <font color='green'><b>{cashier_data.get('certificate_end', 'N/A')}</b></font><br>"
                "<br>================<br>"
            )

            self.info_text.setHtml(info)

        except requests.RequestException as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося отримати інформацію про касира: {e}")

    def get_taxes_info(self, access_token):
        """Отримує інформацію про податкові ставки і оновлює текстовий блок"""
        api_url = self.api_url.text()

        headers = {
            'accept': 'application/json',
            'X-Client-Name': 'Test-Client-Name',
            'X-Client-Version': 'Test-Client-Version',
            'Authorization': f'Bearer {access_token}'
        }

        try:
            response = requests.get(f"{api_url}/api/v1/cashier/tax", headers=headers)
            response.raise_for_status()  # Перевірка наявності помилок HTTP

            taxes_data = response.json()

            # Форматування даних для відображення
            taxes_info = ""
            for tax in taxes_data:
                taxes_info += (
                    f"<b>Код:</b> <font color='green'><b>{tax.get('code', 'N/A')}</b></font><br>"
                    f"<b>Назва:</b> <font color='green'><b>{tax.get('label', 'N/A')}</b></font><br>"
                    f"<b>Літера:</b> <font color='green'><b>{tax.get('symbol', 'N/A')}</b></font><br>"
                    f"<b>ПДВ:</b> <font color='green'><b>{tax.get('rate', 0)}%</b></font><br>"
                    f"<b>Акцизний збір:</b> <font color='green'><b>{tax.get('extra_rate', 0)}%</b></font><br>"
                    f"<b>Створено:</b> <font color='green'><b>{tax.get('created_at', 'N/A')}</b></font><br>"
                    f"<b>Оновлено:</b> <font color='green'><b>{tax.get('updated_at', 'N/A')}</b></font><br>"
                    "<br>================<br>"
                )

            self.info_text.append(taxes_info)

        except requests.RequestException as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося отримати інформацію про податкові ставки: {e}")

    def center_on_parent(self, parent):
        """Центрує вікно на батьківському вікні."""
        parent_rect = parent.geometry()
        dialog_rect = self.geometry()

        x = parent_rect.left() + (parent_rect.width() - dialog_rect.width()) / 2
        y = parent_rect.top() + (parent_rect.height() - dialog_rect.height()) / 2

        return QRect(int(x), int(y), dialog_rect.width(), dialog_rect.height())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Створюємо батьківське вікно для прикладу
    parent_window = QDialog()
    parent_window.setWindowTitle("Батьківське вікно")
    parent_window.setGeometry(100, 100, 800, 600)
    parent_window.show()

    dialog = CheckboxSettingsDialog(parent=parent_window)
    dialog.exec_()
