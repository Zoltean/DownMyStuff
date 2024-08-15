import sqlite3
import pandas as pd
import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QFileDialog, QMessageBox, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from .add_contact import AddContactDialog
from .edit_contact import EditContactDialog
from .IEContacts import IEContacts  # Додаємо імпорт нового класу

class ContactsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Контакти")
        self.setGeometry(200, 200, 900, 600)

        # Ініціалізація IEContacts перед іншими компонентами
        self.ie_contacts = IEContacts(self)

        self.add_button = QPushButton("Додати")
        self.search_button = QPushButton("Шукати")
        self.reset_search_button = QPushButton("Зкинути фільтр")
        self.import_button = QPushButton("Імпорт з Excel")
        self.export_button = QPushButton("Експорт в Excel")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введіть текст для пошуку")
        self.search_input.textChanged.connect(self.search_contact)

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
        self.reset_search_button.clicked.connect(self.reset_search)

        self.import_button.clicked.connect(self.ie_contacts.import_contacts)
        self.export_button.clicked.connect(self.ie_contacts.export_contacts)

        if parent:
            qr = parent.frameGeometry()
            cp = qr.center()
            self.move(cp - self.rect().center())

    def search_contact(self):
        search_query = self.search_input.text().strip()
        self.load_data(search_query)

    def load_data(self, search_query=''):
        try:
            db_path = self.ie_contacts.get_db_path()
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

    def reset_search(self):
        self.search_input.clear()
        self.load_data()

    def open_edit_contact_dialog(self, row, column):
        contact_id = self.table.item(row, 0).text()
        dialog = EditContactDialog(self, contact_id)
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()
