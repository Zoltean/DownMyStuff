from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QPoint

class AddContactDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Додати Контакт")
        self.setGeometry(300, 300, 400, 300)  # Початкові координати та розмір

        # Створити поля для введення даних контакту
        self.form_layout = QFormLayout()
        self.sename_input = QLineEdit()
        self.name_input = QLineEdit()
        self.f_name_input = QLineEdit()
        self.phone_number_input = QLineEdit()
        self.address_input = QLineEdit()
        self.address_NP_input = QLineEdit()
        self.email_input = QLineEdit()
        self.form_layout.addRow("Прізвище", self.sename_input)
        self.form_layout.addRow("Ім'я", self.name_input)
        self.form_layout.addRow("По батькові", self.f_name_input)
        self.form_layout.addRow("Телефон", self.phone_number_input)
        self.form_layout.addRow("Адреса", self.address_input)
        self.form_layout.addRow("Адреса НП", self.address_NP_input)
        self.form_layout.addRow("Email", self.email_input)

        # Кнопки для збереження та скасування
        self.save_button = QPushButton("Зберегти")
        self.cancel_button = QPushButton("Скасувати")
        self.save_button.clicked.connect(self.save_contact)
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

    def save_contact(self):
        # Логіка для збереження контакту
        # Тут можна додати код для збереження в базу даних або іншій дії
        self.accept()
