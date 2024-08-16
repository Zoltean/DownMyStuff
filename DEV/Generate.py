import sys
import hashlib
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QClipboard, QGuiApplication

class LicenseGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.license_key = None  # Атрибут для зберігання згенерованого ключа

    def init_ui(self):
        layout = QVBoxLayout()

        self.device_id_input = QLineEdit(self)
        self.device_id_input.setPlaceholderText("Введіть DEVICE_ID")

        self.months_input = QLineEdit(self)
        self.months_input.setPlaceholderText("Введіть термін ліцензії в місяцях")

        self.generate_button = QPushButton("Генерувати ключ", self)
        self.generate_button.clicked.connect(self.generate_key)

        self.result_label = QLabel(self)

        self.copy_button = QPushButton("Копіювати ключ в буфер обміну", self)
        self.copy_button.clicked.connect(self.copy_to_clipboard)

        layout.addWidget(self.device_id_input)
        layout.addWidget(self.months_input)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.copy_button)

        self.setLayout(layout)
        self.setWindowTitle("Генератор ліцензійних ключів")
        self.show()

    def generate_license_key(self, device_id, months):
        """Генерує ліцензійний ключ на основі DEVICE_ID та терміна ліцензії."""
        expiration_date = datetime.now() + timedelta(days=31 * months)
        raw_key = f"{device_id}-{expiration_date.strftime('%Y-%m-%d')}-{months}"
        license_key = hashlib.sha256(raw_key.encode()).hexdigest()
        return license_key

    def verify_license_key(self, device_id, license_key, months):
        """Перевіряє ліцензійний ключ на основі DEVICE_ID та терміна ліцензії."""
        expiration_date = datetime.now() + timedelta(days=31 * months)
        raw_key = f"{device_id}-{expiration_date.strftime('%Y-%m-%d')}-{months}"
        expected_key = hashlib.sha256(raw_key.encode()).hexdigest()
        return expected_key == license_key

    def generate_key(self):
        device_id = self.device_id_input.text()
        try:
            months = int(self.months_input.text())
            if months <= 0:
                self.result_label.setText("Кількість місяців повинна бути додатною.")
                return

            self.license_key = self.generate_license_key(device_id, months)
            is_valid = self.verify_license_key(device_id, self.license_key, months)
            self.result_label.setText(f"Сгенерований ключ ліцензії на {months} місяців:\n{self.license_key}\n\nЧи є ключ ліцензії дійсним: {is_valid}")

        except ValueError:
            self.result_label.setText("Будь ласка, введіть коректне число для терміну ліцензії.")

    def copy_to_clipboard(self):
        if self.license_key:
            clipboard = QGuiApplication.clipboard()
            clipboard.setText(self.license_key)
            self.result_label.setText("Ключ скопійовано в буфер обміну.")
        else:
            self.result_label.setText("Спочатку згенеруйте ключ.")

def main():
    app = QApplication(sys.argv)
    ex = LicenseGeneratorApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
