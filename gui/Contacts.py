import sqlite3
import os
import logging
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import pandas as pd
from .add_contact import AddContactDialog

class ContactsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Контакти")
        self.setGeometry(200, 200, 600, 400)

        # Створити кнопки
        self.add_button = QPushButton("Додати")
        self.edit_button = QPushButton("Змінити")
        self.delete_button = QPushButton("Видалити")
        self.search_button = QPushButton("Шукати")
        self.import_button = QPushButton("Імпорт з Excel")
        self.export_button = QPushButton("Експорт в Excel")

        # Налаштування шрифту для всіх кнопок
        font = QFont("Arial", 12)
        for button in [self.add_button, self.edit_button, self.delete_button,
                       self.search_button, self.import_button, self.export_button]:
            button.setFont(font)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Макет з використанням QVBoxLayout
        layout = QVBoxLayout()
        layout.addWidget(self.add_button)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.search_button)
        layout.addWidget(self.import_button)
        layout.addWidget(self.export_button)
        layout.addStretch()  # Додає відступ, щоб кнопки займали весь вільний простір

        self.setLayout(layout)

        # Підключити сигнали
        self.add_button.clicked.connect(self.open_add_contact_dialog)  # Оновлений обробник
        self.edit_button.clicked.connect(self.edit_contact)
        self.delete_button.clicked.connect(self.delete_contact)
        self.search_button.clicked.connect(self.search_contact)
        self.import_button.clicked.connect(self.import_contacts)
        self.export_button.clicked.connect(self.export_contacts)

        # Центрування вікна по центру батьківського вікна
        if parent:
            qr = parent.frameGeometry()
            cp = qr.center()
            self.move(cp - self.rect().center())

    def open_add_contact_dialog(self):
        dialog = AddContactDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Логіка для обробки збереження нового контакту
            QMessageBox.information(self, "Інформація", "Контакт додано.")  # Приклад повідомлення

    def add_contact(self):
        # Логіка для додавання контакту
        pass

    def edit_contact(self):
        # Логіка для редагування контакту
        pass

    def delete_contact(self):
        # Логіка для видалення контакту
        pass

    def search_contact(self):
        # Логіка для пошуку контакту
        pass

    def import_contacts(self):
        # Логіка для імпорту контактів з Excel
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Імпортувати з Excel", "",
                                                   "Excel Files (*.xlsx);;All Files (*)", options=options)
        if file_name:
            try:
                df = pd.read_excel(file_name)
                # Тривіальний приклад імпорту даних
                with sqlite3.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                  'database.db')) as connection:
                    df.to_sql('contacts', connection, if_exists='append', index=False)
                QMessageBox.information(self, "Успіх", "Контакти успішно імпортовані.")
            except Exception as e:
                QMessageBox.critical(self, "Помилка", f"Помилка імпорту: {e}")

    def export_contacts(self):
        # Логіка для експорту контактів в Excel
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Експортувати в Excel", "",
                                                   "Excel Files (*.xlsx);;All Files (*)", options=options)
        if file_name:
            try:
                with sqlite3.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                  'database.db')) as connection:
                    df = pd.read_sql("SELECT * FROM contacts", connection)
                    df.to_excel(file_name, index=False)
                QMessageBox.information(self, "Успіх", "Контакти успішно експортовані.")
            except Exception as e:
                QMessageBox.critical(self, "Помилка", f"Помилка експорту: {e}")

    def init_db(self):
        """Перевіряє наявність таблиці 'contacts' у базі даних та створює її, якщо її немає."""
        # Отримати директорію батьківської папки
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(BASE_DIR, 'database.db')

        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()

            # SQL для перевірки наявності таблиці
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sename TEXT NOT NULL,
                    name TEXT NOT NULL,
                    f_name TEXT NOT NULL,
                    phone_number TEXT NOT NULL,
                    address TEXT,
                    address_NP TEXT,
                    email TEXT
                )
            """)
            connection.commit()
            logging.info("Таблиця 'contacts' успішно створена або вже існує.")
        except sqlite3.DatabaseError as e:
            logging.error(f"Помилка при виконанні SQL запиту: {e}")
            raise
        except Exception as e:
            logging.error(f"Неочікувана помилка: {e}")
            raise
        finally:
            try:
                connection.close()
            except NameError:
                # Якщо з'єднання не було створено
                logging.warning("З'єднання з базою даних не було створено.")
            except sqlite3.Error as e:
                logging.error(f"Помилка при закритті з'єднання з базою даних: {e}")
