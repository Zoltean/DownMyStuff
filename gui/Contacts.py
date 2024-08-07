import sqlite3
import os
import logging
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QCoreApplication

# Налаштування логування для консолі
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class ContactsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Контакти")
        self.setGeometry(200, 200, 400, 300)

        try:
            self.init_db()
        except Exception as e:
            logging.error(f"Помилка при ініціалізації бази даних: {e}")
            self.info_label.setText("Не вдалося ініціалізувати базу даних. Перевірте консоль для деталей.")

        layout = QVBoxLayout()

        self.info_label = QLabel("Тут буде інформація про контакти")
        layout.addWidget(self.info_label)

        self.close_button = QPushButton("Закрити")
        self.close_button.clicked.connect(self.accept)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.center()

    def center(self):
        screen_rect = QCoreApplication.instance().primaryScreen().geometry()
        dialog_rect = self.geometry()
        x = (screen_rect.width() - dialog_rect.width()) / 2
        y = (screen_rect.height() - dialog_rect.height()) / 2
        self.move(int(x), int(y))

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
