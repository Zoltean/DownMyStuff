import sqlite3
import requests
from PyQt5.QtWidgets import QMessageBox

class CheckboxSettingsLogic:
    def __init__(self, dialog):
        self.dialog = dialog
        self.access_token = None

    def load_settings_from_db(self):
        """Завантажує налаштування з бази даних і заповнює поля форми."""
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            cursor.execute(
                'SELECT license_key, cashier_login, cashier_password, access_token FROM checkbox_settings ORDER BY id DESC LIMIT 1')
            row = cursor.fetchone()

            if row:
                license_key, cashier_login, cashier_password, access_token = row
                self.dialog.license_key.setText(license_key)
                self.dialog.cashier_login.setText(cashier_login)
                self.dialog.cashier_password.setText(cashier_password)

                self.access_token = access_token  # Збережіть токен у властивості

                # Передайте токен у методи, які його потребують
                if self.access_token:
                    self.get_cashier_info(self.access_token)
                    self.get_taxes_info(self.access_token)

            conn.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self.dialog, "Помилка", f"Не вдалося зчитати налаштування з бази даних: {e}")

    def authenticate(self):
        api_url = self.dialog.api_url.text()
        license_key = self.dialog.license_key.text()
        login = self.dialog.cashier_login.text()
        password = self.dialog.cashier_password.text()

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
            response.raise_for_status()

            response_data = response.json()
            access_token = response_data.get('access_token')

            if response.status_code == 200:
                QMessageBox.information(self.dialog, "Авторизація успішна", f"Токен доступу: {access_token}")
                self.save_settings_to_db(license_key, login, password, access_token)

                # Передайте токен у методи
                self.get_cashier_info(access_token)
                self.get_taxes_info(access_token)
            else:
                QMessageBox.warning(self.dialog, "Помилка авторизації", f"Помилка: {response.text}")

        except requests.RequestException as e:
            QMessageBox.critical(self.dialog, "Помилка", f"Не вдалося здійснити запит: {e}")

    def save_settings_to_db(self, license_key, login, password, access_token):
        """Зберігає налаштування у базі даних"""
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS checkbox_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    license_key TEXT,
                    cashier_login TEXT,
                    cashier_password TEXT,
                    access_token TEXT
                )
            ''')

            cursor.execute('''
                INSERT INTO checkbox_settings (license_key, cashier_login, cashier_password, access_token)
                VALUES (?, ?, ?, ?)
            ''', (license_key, login, password, access_token))

            conn.commit()
            conn.close()

            QMessageBox.information(self.dialog, "Успішно", "Налаштування збережено в базі даних.")

        except sqlite3.Error as e:
            QMessageBox.critical(self.dialog, "Помилка", f"Не вдалося зберегти налаштування в базі даних: {e}")

    def get_cashier_info(self, access_token):
        """Отримує інформацію про касира і оновлює текстовий блок"""
        api_url = self.dialog.api_url.text()

        headers = {
            'accept': 'application/json',
            'X-Client-Name': 'Test-Client-Name',
            'X-Client-Version': 'Test-Client-Version',
            'Authorization': f'Bearer {access_token}'
        }

        try:
            response = requests.get(f"{api_url}/api/v1/cashier/me", headers=headers)
            response.raise_for_status()

            cashier_data = response.json()

            organization = cashier_data.get('organization', {})
            info = (
                f"<b>Назва організації:</b> <font color='green'><b>{organization.get('title', 'N/A')}</b></font><br>"
                f"<b>ЕДРПОУ:</b> <font color='green'><b>{organization.get('edrpou', 'N/A')}</b></font><br>"
                f"<b>Податкові ставки:</b> <font color='green'><b>{organization.get('tax_number', 'N/A')}</b></font><br>"
                f"<b>Ім'я касира:</b> <font color='green'><b>{cashier_data.get('full_name', 'N/A')}</b></font><br>"
                f"<b>Срок дії ключа:</b> <font color='green'><b>{cashier_data.get('certificate_end', 'N/A')}</b></font><br>"
                "<br>================<br>"
            )

            self.dialog.info_text.setHtml(info)

        except requests.RequestException as e:
            QMessageBox.critical(self.dialog, "Помилка", f"Не вдалося отримати інформацію про касира: {e}")

    def get_taxes_info(self, access_token):
        """Отримує інформацію про податкові ставки і оновлює текстовий блок"""
        api_url = self.dialog.api_url.text()

        headers = {
            'accept': 'application/json',
            'X-Client-Name': 'Test-Client-Name',
            'X-Client-Version': 'Test-Client-Version',
            'Authorization': f'Bearer {access_token}'
        }

        try:
            response = requests.get(f"{api_url}/api/v1/cashier/tax", headers=headers)
            response.raise_for_status()

            taxes_data = response.json()

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

            self.dialog.info_text.append(taxes_info)

        except requests.RequestException as e:
            QMessageBox.critical(self.dialog, "Помилка", f"Не вдалося отримати інформацію про податкові ставки: {e}")
