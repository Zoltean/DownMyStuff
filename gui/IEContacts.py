import pandas as pd
import sqlite3
import os
import re
from PyQt5.QtWidgets import QFileDialog, QMessageBox

class IEContacts:
    def __init__(self, parent=None):
        self.parent = parent

    def import_contacts(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self.parent, "Імпортувати з Excel", "",
                                                   "Excel Files (*.xlsx);;All Files (*)", options=options)
        if file_name:
            try:
                # Читання Excel з текстовими стовпцями для телефонних номерів
                df = pd.read_excel(file_name, dtype=str)

                # Виведення списку стовпців для перевірки
                print("Стовпці у файлі Excel:", df.columns.tolist())

                # Валідація Excel даних
                validation_errors = self.validate_excel_data(df)
                if validation_errors:
                    error_message = "\n".join(validation_errors)
                    QMessageBox.warning(self.parent, "Помилка валідації", f"Файл містить помилки:\n{error_message}\nІмпорт скасовано.")
                    return

                # Форматування телефонних номерів
                df['Номер телефону'] = df['Номер телефону'].apply(self.format_phone_number)

                # Перейменування колонок
                df.rename(columns={
                    'Прізвище': 'sename',
                    'Ім\'я': 'name',
                    'По-батькові': 'f_name',
                    'Номер телефону': 'phone_number',
                    'Місто': 'address',
                    'Номер відділення': 'address_NP',
                    'Email': 'email'
                }, inplace=True)

                # Видалення стовпця 'id' якщо існує
                if 'id' in df.columns:
                    df.drop(columns=['id'], inplace=True)

                with sqlite3.connect(self.get_db_path()) as connection:
                    df.to_sql('contacts', connection, if_exists='append', index=False, method='multi')

                self.parent.load_data()
                QMessageBox.information(self.parent, "Успіх", "Контакти успішно імпортовані.")
            except Exception as e:
                QMessageBox.critical(self.parent, "Помилка", f"Помилка імпорту: {e}")

    def export_contacts(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self.parent, "Експортувати в Excel", "",
                                                   "Excel Files (*.xlsx);;All Files (*)", options=options)
        if file_name:
            try:
                with sqlite3.connect(self.get_db_path()) as connection:
                    df = pd.read_sql("SELECT sename, name, f_name, phone_number, address, address_NP, email FROM contacts", connection)
                    df.rename(columns={
                        'sename': 'Прізвище',
                        'name': 'Ім\'я',
                        'f_name': 'По-батькові',
                        'phone_number': 'Номер телефону',
                        'address': 'Місто',
                        'address_NP': 'Номер відділення',
                        'email': 'Email'
                    }, inplace=True)
                    df.to_excel(file_name, index=False)
                QMessageBox.information(self.parent, "Успіх", "Контакти успішно експортовані.")
            except Exception as e:
                QMessageBox.critical(self.parent, "Помилка", f"Помилка експорту: {e}")

    def validate_excel_data(self, df):
        errors = []

        # Перевірка наявності обов'язкових стовпців, окрім 'Email'
        required_columns = ['Прізвище', 'Ім\'я', 'По-батькові', 'Номер телефону', 'Місто', 'Номер відділення']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            errors.append(f"Відсутні стовпці: {', '.join(missing_columns)}")

        # Перевірка формату телефонних номерів
        if 'Номер телефону' in df.columns:
            phone_numbers = df['Номер телефону']
            for idx, number in phone_numbers.items():
                if not self.is_valid_phone_number(number):
                    errors.append(f"Некоректний телефонний номер у рядку {idx + 1}: {number}")

        return errors

    def is_valid_phone_number(self, number):
        digits = re.sub(r'\D', '', number)
        return len(digits) in [9, 12] and (digits.startswith('380') or len(digits) == 9)

    def format_phone_number(self, number):
        # Видаляємо всі символи, крім цифр
        digits = re.sub(r'\D', '', number)
        # Перевіряємо, чи номер починається з 380
        if digits.startswith('380'):
            return f"+{digits}"
        # Додаємо код країни, якщо його немає
        if len(digits) == 9:
            return f"+380{digits}"
        # Повертаємо номер без змін, якщо не відповідає формату
        return number

    def get_db_path(self):
        return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database.db')
