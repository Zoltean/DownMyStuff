from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QPushButton, QFormLayout, QSizePolicy, QMessageBox)
from PyQt5.QtGui import QFont
import sqlite3

class AddGoodsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Додати Товар")
        self.setGeometry(300, 300, 400, 300)  # Початкові координати та розмір

        # Створити поля для введення даних товару
        self.form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.group_name_input = QLineEdit()
        self.tax_input = QLineEdit()
        self.UKTZED_input = QLineEdit()
        self.price_input = QLineEdit()
        self.quantity_input = QLineEdit()

        self.form_layout.addRow("Назва", self.name_input)
        self.form_layout.addRow("Група", self.group_name_input)
        self.form_layout.addRow("Податок", self.tax_input)
        self.form_layout.addRow("UKTZED", self.UKTZED_input)
        self.form_layout.addRow("Ціна", self.price_input)
        self.form_layout.addRow("Кількість", self.quantity_input)

        # Кнопки для збереження та скасування
        self.save_button = QPushButton("Зберегти")
        self.cancel_button = QPushButton("Скасувати")
        self.save_button.clicked.connect(self.save_goods)
        self.cancel_button.clicked.connect(self.reject)

        # Налаштування шрифтів для кнопок
        font = QFont("Arial", 12)
        self.save_button.setFont(font)
        self.cancel_button.setFont(font)
        self.save_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.cancel_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Додати кнопки до макету
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        # Основний макет
        layout = QVBoxLayout()
        layout.addLayout(self.form_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Центрування діалогу
        if parent:
            self.center_on_parent(parent)

    def center_on_parent(self, parent):
        """Центрує діалогове вікно відносно батьківського вікна."""
        parent_rect = parent.geometry()
        dialog_rect = self.geometry()
        x = parent_rect.left() + (parent_rect.width() - dialog_rect.width()) / 2
        y = parent_rect.top() + (parent_rect.height() - dialog_rect.height()) / 2
        self.move(int(x), int(y))

    def validate_and_correct_data(self):
        """Перевіряє і виправляє введені дані."""
        name = self.name_input.text().strip()
        group_name = self.group_name_input.text().strip()
        tax = self.tax_input.text().strip()
        UKTZED = self.UKTZED_input.text().strip()
        price = self.price_input.text().strip()
        quantity = self.quantity_input.text().strip()

        # Перевірка на обов'язкові поля
        if not name:
            QMessageBox.warning(self, "Помилка", "Назва є обов'язковим полем.")
            return None, None, None, None, None, None
        if not price:
            QMessageBox.warning(self, "Помилка", "Ціна є обов'язковим полем.")
            return None, None, None, None, None, None
        if not quantity:
            QMessageBox.warning(self, "Помилка", "Кількість є обов'язковим полем.")
            return None, None, None, None, None, None

        # Перевірка формату даних
        try:
            tax = int(tax) if tax else 0  # Перетворення tax в int
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            QMessageBox.warning(self, "Помилка", "Невірний формат числових значень.")
            return None, None, None, None, None, None

        return name, group_name, tax, UKTZED, price, quantity

    def save_goods(self):
        """Зберігає товар у базу даних."""
        name, group_name, tax, UKTZED, price, quantity = self.validate_and_correct_data()

        if name is not None:
            try:
                with sqlite3.connect('database.db') as connection:
                    cursor = connection.cursor()
                    # Вставка даних до бази даних з використанням параметризованих запитів
                    cursor.execute("""
                        INSERT INTO goods (name, group_name, tax, UKTZED, price, quantity)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (name, group_name, tax, UKTZED, price, quantity))
                    connection.commit()
                QMessageBox.information(self, "Успіх", "Товар успішно додано.")
                self.accept()
            except sqlite3.DatabaseError as e:
                QMessageBox.critical(self, "Помилка", f"Помилка при збереженні товару: {e}")
