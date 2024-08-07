from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QPushButton, QFormLayout, QSizePolicy, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sqlite3
import re

class EditContactDialog(QDialog):
    def __init__(self, parent=None, contact_id=None):
        super().__init__(parent)
        self.contact_id = contact_id
        self.setWindowTitle("Редагувати Контакт")
        self.setGeometry(300, 300, 400, 300)  # Початкові координати та розмір

        # Створити поля для введення даних контакту
        self.form_layout = QFormLayout()
        self.sename_input = QLineEdit()
        self.name_input = QLineEdit()
        self.f_name_input = QLineEdit()
        self.phone_number_input = QLineEdit()
        self.address_input = QLineEdit()  # Місто
        self.address_NP_input = QLineEdit()  # Відділення НП
        self.email_input = QLineEdit()

        self.form_layout.addRow("Прізвище", self.sename_input)
        self.form_layout.addRow("Ім'я", self.name_input)
        self.form_layout.addRow("По батькові", self.f_name_input)
        self.form_layout.addRow("Телефон", self.phone_number_input)
        self.form_layout.addRow("Місто", self.address_input)  # Замінено "Адреса" на "Місто"
        self.form_layout.addRow("Відділення НП", self.address_NP_input)  # Замінено "Адреса НП" на "Відділення НП"
        self.form_layout.addRow("Email", self.email_input)

        # Налаштування маски для номера телефону
        self.phone_number_input.setInputMask("+38 000 000 00 00;_")
        self.phone_number_input.setPlaceholderText("Введіть номер телефону")
        self.phone_number_input.setStyleSheet("color: black; background-color: white;")

        # Кнопки для збереження, видалення та скасування
        self.save_button = QPushButton("Редагувати")
        self.delete_button = QPushButton("Видалити контакт повністю")
        self.cancel_button = QPushButton("Скасувати")
        self.save_button.clicked.connect(self.save_contact)
        self.delete_button.clicked.connect(self.confirm_delete_contact)
        self.cancel_button.clicked.connect(self.reject)

        # Налаштування шрифтів для кнопок
        font = QFont("Arial", 12)
        self.save_button.setFont(font)
        self.delete_button.setFont(font)
        self.cancel_button.setFont(font)
        self.save_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.delete_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.cancel_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Налаштування кольору кнопки "Видалити"
        self.delete_button.setStyleSheet("background-color: red; color: white;")

        # Додати кнопки до макету
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.cancel_button)

        # Основний макет
        layout = QVBoxLayout()
        layout.addLayout(self.form_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Центрування діалогу
        if parent:
            self.center_on_parent(parent)

        # Завантажити дані контакту
        self.load_contact()

    def center_on_parent(self, parent):
        """Центрує діалогове вікно відносно батьківського вікна."""
        parent_rect = parent.geometry()
        dialog_rect = self.geometry()
        x = parent_rect.left() + (parent_rect.width() - dialog_rect.width()) / 2
        y = parent_rect.top() + (parent_rect.height() - dialog_rect.height()) / 2
        self.move(int(x), int(y))

    def load_contact(self):
        """Завантажує дані контакту з бази даних."""
        try:
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT sename, name, f_name, phone_number, address, address_NP, email FROM contacts WHERE id = ?", (self.contact_id,))
                contact = cursor.fetchone()
                if contact:
                    self.sename_input.setText(contact[0])
                    self.name_input.setText(contact[1])
                    self.f_name_input.setText(contact[2])
                    self.phone_number_input.setText(contact[3])
                    self.address_input.setText(contact[4])
                    self.address_NP_input.setText(contact[5])
                    self.email_input.setText(contact[6])
                else:
                    QMessageBox.warning(self, "Помилка", "Контакт не знайдено.")
                    self.reject()
        except sqlite3.DatabaseError as e:
            QMessageBox.critical(self, "Помилка", f"Помилка при завантаженні даних контакту: {e}")

    def validate_and_correct_data(self):
        """Перевіряє і виправляє введені дані."""
        sename = self.sename_input.text().strip()
        name = self.name_input.text().strip()
        f_name = self.f_name_input.text().strip()
        phone_number = self.phone_number_input.text().strip()
        address = self.address_input.text().strip()  # Місто
        address_NP = self.address_NP_input.text().strip()  # Відділення НП
        email = self.email_input.text().strip()

        # Перевірка і виправлення першої літери у верхній регістр
        sename = sename.capitalize()
        name = name.capitalize()
        f_name = f_name.capitalize()

        # Перевірка формату номера телефону
        phone_number = re.sub(r'\s+', '', phone_number)  # Видалити всі пробіли
        if not re.match(r'^\+380\d{9}$', phone_number):
            QMessageBox.warning(self, "Помилка", "Неправильний формат номера телефону. Повинен бути +38 0хх ххх хх хх.")
            return None, None, None, None, None, None, None

        return sename, name, f_name, phone_number, address, address_NP, email

    def save_contact(self):
        """Зберігає контакт у базу даних."""
        sename, name, f_name, phone_number, address, address_NP, email = self.validate_and_correct_data()

        if sename is not None:
            try:
                with sqlite3.connect('database.db') as connection:
                    cursor = connection.cursor()
                    # Оновлення даних у базі даних
                    cursor.execute("""
                        UPDATE contacts
                        SET sename = ?, name = ?, f_name = ?, phone_number = ?, address = ?, address_NP = ?, email = ?
                        WHERE id = ?
                    """, (sename, name, f_name, phone_number, address, address_NP, email, self.contact_id))
                    connection.commit()
                QMessageBox.information(self, "Успіх", "Контакт успішно оновлено.")
                self.accept()
            except sqlite3.DatabaseError as e:
                QMessageBox.critical(self, "Помилка", f"Помилка при оновленні контакту: {e}")

    def confirm_delete_contact(self):
        """Показує діалог підтвердження видалення контакту."""
        sename = self.sename_input.text().strip()
        name = self.name_input.text().strip()
        f_name = self.f_name_input.text().strip()
        full_name = f"{sename} {name} {f_name}"

        reply = QMessageBox.question(self, "Підтвердження видалення",
                                     f"Ви дійсно бажаєте видалити контакт {full_name}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.delete_contact()

    def delete_contact(self):
        """Видаляє контакт з бази даних."""
        try:
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM contacts WHERE id = ?", (self.contact_id,))
                connection.commit()
            QMessageBox.information(self, "Успіх", "Контакт успішно видалено.")
            self.accept()
        except sqlite3.DatabaseError as e:
            QMessageBox.critical(self, "Помилка", f"Помилка при видаленні контакту: {e}")
