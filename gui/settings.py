import sys
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFormLayout, QApplication, QSizePolicy
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QRect
from .CheckboxSettings import CheckboxSettingsDialog  # Імпортуємо новий клас


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Налаштування")
        self.setGeometry(0, 0, 350, 150)  # Початкові розміри вікна

        # Створення компонентів інтерфейсу
        layout = QVBoxLayout()

        # Створення кнопок
        button_layout = QVBoxLayout()

        # Кнопка "Нова Пошта"
        self.nova_posta_button = QPushButton("Нова Пошта")
        self.nova_posta_button.setIcon(QIcon("ico/Nova.png"))  # Вказати шлях до іконки
        self.nova_posta_button.setFont(QFont("Arial", 10))  # Встановити шрифт
        self.nova_posta_button.setFixedSize(110, 30)  # Встановити розмір кнопки
        self.nova_posta_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.nova_posta_button.clicked.connect(self.handle_nova_posta)
        button_layout.addWidget(self.nova_posta_button)

        # Кнопка "Checkbox"
        self.checkbox_button = QPushButton("Checkbox")
        self.checkbox_button.setIcon(QIcon("ico/checkbox.jpg"))  # Вказати шлях до іконки
        self.checkbox_button.setFont(QFont("Arial", 10))  # Встановити шрифт
        self.checkbox_button.setFixedSize(110, 30)  # Встановити розмір кнопки
        self.checkbox_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.checkbox_button.clicked.connect(self.handle_checkbox)
        button_layout.addWidget(self.checkbox_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Центрування вікна відносно батьківського вікна
        if parent:
            self.setGeometry(self.center_on_parent(parent))

    def handle_nova_posta(self):
        print("Нова Пошта натиснуто")

    def handle_checkbox(self):
        # Закриття поточного вікна
        self.accept()
        # Відкриття нового вікна
        dialog = CheckboxSettingsDialog(parent=self.parent())
        dialog.exec_()

    def center_on_parent(self, parent):
        """Центрує вікно на батьківському вікні."""
        parent_rect = parent.geometry()
        dialog_rect = self.geometry()

        x = parent_rect.left() + (parent_rect.width() - dialog_rect.width()) / 2
        y = parent_rect.top() + (parent_rect.height() - dialog_rect.height()) / 2

        return QRect(int(x), int(y), dialog_rect.width(), dialog_rect.height())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Створюємо батьківське вікно для прикладу
    parent_window = QDialog()
    parent_window.setWindowTitle("Батьківське вікно")
    parent_window.setGeometry(100, 100, 800, 600)
    parent_window.show()

    dialog = SettingsDialog(parent=parent_window)
    dialog.exec_()
