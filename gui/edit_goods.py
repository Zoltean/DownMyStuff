import sqlite3
import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QPushButton, QFormLayout, QSizePolicy, QMessageBox)
from PyQt5.QtGui import QFont

class EditGoodsDialog(QDialog):
    def __init__(self, parent=None, goods_id=None):
        super().__init__(parent)
        self.goods_id = goods_id
        self.setWindowTitle("Редагувати Товар")
        self.setGeometry(300, 300, 400, 300)

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

        self.save_button = QPushButton("Редагувати")
        self.delete_button = QPushButton("Видалити товар повністю")
        self.cancel_button = QPushButton("Скасувати редагування")
        self.save_button.clicked.connect(self.save_goods)
        self.delete_button.clicked.connect(self.confirm_delete_goods)
        self.cancel_button.clicked.connect(self.reject)

        font = QFont("Arial", 12)
        self.save_button.setFont(font)
        self.delete_button.setFont(font)
        self.cancel_button.setFont(font)
        self.save_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.delete_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.cancel_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.delete_button.setStyleSheet("background-color: red; color: white;")

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.cancel_button)

        layout = QVBoxLayout()
        layout.addLayout(self.form_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.load_data()

        # Центрування діалогового вікна
        if parent:
            self.center_on_parent(parent)

    def center_on_parent(self, parent):
        """Центрує діалогове вікно відносно батьківського вікна."""
        parent_rect = parent.geometry()
        dialog_rect = self.geometry()
        x = parent_rect.left() + (parent_rect.width() - dialog_rect.width()) / 2
        y = parent_rect.top() + (parent_rect.height() - dialog_rect.height()) / 2
        self.move(int(x), int(y))

    def load_data(self):
        try:
            db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database.db')
            with sqlite3.connect(db_path) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT name, group_name, tax, UKTZED, price, quantity FROM goods WHERE id = ?", (self.goods_id,))
                row = cursor.fetchone()
                if row:
                    self.name_input.setText(row[0])
                    self.group_name_input.setText(row[1])
                    self.tax_input.setText(str(row[2]))  # tax as int
                    self.UKTZED_input.setText(row[3])
                    self.price_input.setText(str(row[4]))
                    self.quantity_input.setText(str(row[5]))
                else:
                    QMessageBox.warning(self, "Помилка", "Товар не знайдено.")
                    self.reject()
        except sqlite3.DatabaseError as e:
            QMessageBox.critical(self, "Помилка", f"Помилка при завантаженні даних: {e}")

    def validate_and_correct_data(self):
        name = self.name_input.text().strip()
        group_name = self.group_name_input.text().strip()
        tax = self.tax_input.text().strip()
        UKTZED = self.UKTZED_input.text().strip()
        price = self.price_input.text().strip()
        quantity = self.quantity_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Помилка", "Назва є обов'язковим полем.")
            return None, None, None, None, None, None
        if not price:
            QMessageBox.warning(self, "Помилка", "Ціна є обов'язковим полем.")
            return None, None, None, None, None, None
        if not quantity:
            QMessageBox.warning(self, "Помилка", "Кількість є обов'язковим полем.")
            return None, None, None, None, None, None

        try:
            tax = int(tax) if tax else 0  # Перетворення tax в int
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            QMessageBox.warning(self, "Помилка", "Невірний формат числових значень.")
            return None, None, None, None, None, None

        return name, group_name, tax, UKTZED, price, quantity

    def save_goods(self):
        name, group_name, tax, UKTZED, price, quantity = self.validate_and_correct_data()

        if name is not None:
            try:
                db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database.db')
                with sqlite3.connect(db_path) as connection:
                    cursor = connection.cursor()
                    cursor.execute("""
                        UPDATE goods
                        SET name = ?, group_name = ?, tax = ?, UKTZED = ?, price = ?, quantity = ?
                        WHERE id = ?
                    """, (name, group_name, tax, UKTZED, price, quantity, self.goods_id))
                    connection.commit()
                QMessageBox.information(self, "Успіх", "Товар успішно оновлено.")
                self.accept()
            except sqlite3.DatabaseError as e:
                QMessageBox.critical(self, "Помилка", f"Помилка при оновленні товару: {e}")

    def confirm_delete_goods(self):
        name = self.name_input.text().strip()
        reply = QMessageBox.question(self, "Підтвердження видалення",
                                     f"Ви дійсно бажаєте видалити товар '{name}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.delete_goods()

    def delete_goods(self):
        try:
            db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database.db')
            with sqlite3.connect(db_path) as connection:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM goods WHERE id = ?", (self.goods_id,))
                connection.commit()
            QMessageBox.information(self, "Успіх", "Товар успішно видалено.")
            self.accept()
        except sqlite3.DatabaseError as e:
            QMessageBox.critical(self, "Помилка", f"Помилка при видаленні товару: {e}")
 