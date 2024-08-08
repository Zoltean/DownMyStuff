import sqlite3
import os
import logging
import pandas as pd
import re
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem,
                             QFileDialog, QMessageBox, QSizePolicy, QLineEdit)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from .add_contact import AddContactDialog
from .edit_contact import EditContactDialog


class ContactsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Контакти")
        self.setGeometry(200, 200, 900, 600)

        self.add_button = QPushButton("Додати")
        self.search_button = QPushButton("Шукати")
        self.reset_search_button = QPushButton("Зкинути фільтр")
        self.import_button = QPushButton("Імпорт з Excel")
        self.export_button = QPushButton("Експорт в Excel")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введіть текст для пошуку")

        font = QFont("Arial", 10)
        for button in [self.add_button, self.search_button, self.reset_search_button, self.import_button, self.export_button]:
            button.setFont(font)
            button.setFixedSize(110, 30)
            button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.import_button)
        button_layout.addWidget(self.export_button)
        button_layout.addStretch()

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.reset_search_button)

        right_layout = QVBoxLayout()
        right_layout.addLayout(search_layout)
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID", "Прізвище", "Ім'я", "По-батькові", "Номер телефону", "Місто", "Номер відділення", "Email"])
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.cellDoubleClicked.connect(self.open_edit_contact_dialog)
        self.load_data()
        right_layout.addWidget(self.table)

        main_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

        self.add_button.clicked.connect(self.open_add_contact_dialog)
        self.search_button.clicked.connect(self.search_contact)
        self.reset_search_button.clicked.connect(self.reset_search)
        self.import_button.clicked.connect(self.import_contacts)
        self.export_button.clicked.connect(self.export_contacts)

        if parent:
            qr = parent.frameGeometry()
            cp = qr.center()
            self.move(cp - self.rect().center())

    def load_data(self, search_query=''):
        try:
            db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database.db')
            with sqlite3.connect(db_path) as connection:
                query = """
                    SELECT id, sename, name, f_name, phone_number, address, address_NP, email
                    FROM contacts
                    WHERE sename LIKE ? OR name LIKE ? OR f_name LIKE ? OR phone_number LIKE ? OR address LIKE ? OR address_NP LIKE ? OR email LIKE ?
                """
                search_query = f'%{search_query}%'
                df = pd.read_sql(query, connection, params=(
                    search_query, search_query, search_query, search_query, search_query, search_query, search_query))

                df = df.fillna('')

                self.table.setRowCount(len(df))

                for row_idx, row in df.iterrows():
                    for col_idx, value in enumerate(row):
                        item = QTableWidgetItem(str(value))
                        self.table.setItem(row_idx, col_idx, item)

                self.table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Помилка при завантаженні даних: {e}")

    def open_add_contact_dialog(self):
        dialog = AddContactDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()

    def search_contact(self):
        search_query = self.search_input.text().strip()
        self.load_data(search_query)

    def reset_search(self):
        self.search_input.clear()
        self.load_data()

    def import_contacts(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Імпортувати з Excel", "",
                                                   "Excel Files (*.xlsx);;All Files (*)", options=options)
        if file_name:
            try:
                df = pd.read_excel(file_name)

                if not self.validate_excel_data(df):
                    QMessageBox.warning(self, "Попередження", "Файл містить потенційно небезпечні дані. Імпорт скасовано.")
                    return

                df.rename(columns={
                    'Прізвище': 'sename',
                    'Ім\'я': 'name',
                    'По-батькові': 'f_name',
                    'Номер телефону': 'phone_number',
                    'Місто': 'address',
                    'Номер відділення': 'address_NP'
                }, inplace=True)

                if 'id' in df.columns:
                    df.drop(columns=['id'], inplace=True)

                with sqlite3.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                  'database.db')) as connection:
                    df.to_sql('contacts', connection, if_exists='append', index=False, method='multi')

                self.load_data()
                QMessageBox.information(self, "Успіх", "Контакти успішно імпортовані.")
            except Exception as e:
                QMessageBox.critical(self, "Помилка", f"Помилка імпорту: {e}")

    def validate_excel_data(self, df):
        return True

    def open_edit_contact_dialog(self, row, column):
        contact_id = self.table.item(row, 0).text()
        dialog = EditContactDialog(self, contact_id)
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()

    def export_contacts(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Експортувати в Excel", "",
                                                   "Excel Files (*.xlsx);;All Files (*)", options=options)
        if file_name:
            try:
                with sqlite3.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                  'database.db')) as connection:
                    df = pd.read_sql("SELECT sename, name, f_name, phone_number, address, address_NP, email FROM contacts", connection)
                    df.rename(columns={
                        'sename': 'Прізвище',
                        'name': 'Ім\'я',
                        'f_name': 'По-батькові',
                        'phone_number': 'Номер телефону',
                        'address': 'Місто',
                        'address_NP': 'Номер відділення'
                    }, inplace=True)
                    df.to_excel(file_name, index=False)
                QMessageBox.information(self, "Успіх", "Контакти успішно експортовані.")
            except Exception as e:
                QMessageBox.critical(self, "Помилка", f"Помилка експорту: {e}")

    def init_db(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(BASE_DIR, 'database.db')

        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()

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
                logging.warning("З'єднання з базою даних не було створено.")
            except sqlite3.Error as e:
                logging.error(f"Помилка при закритті з'єднання з базою даних: {e}")
