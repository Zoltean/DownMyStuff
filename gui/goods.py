import sqlite3
import os
import pandas as pd
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem,
                             QMessageBox, QSizePolicy, QLineEdit)
from PyQt5.QtGui import QFont
from .add_goods import AddGoodsDialog
from .edit_goods import EditGoodsDialog
from .IEGoods import IEGoods

class GoodsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Товари")
        self.setGeometry(200, 200, 900, 600)

        self.add_button = QPushButton("Додати")
        self.reset_search_button = QPushButton("Зкинути фільтр")
        self.import_button = QPushButton("Імпорт з Excel")
        self.export_button = QPushButton("Експорт в Excel")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введіть текст для пошуку")

        font = QFont("Arial", 10)
        for button in [self.add_button, self.reset_search_button, self.import_button, self.export_button]:
            button.setFont(font)
            button.setFixedSize(110, 30)
            button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Підписка на сигнал textChanged
        self.search_input.textChanged.connect(self.search_goods)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.import_button)
        button_layout.addWidget(self.export_button)
        button_layout.addStretch()

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.reset_search_button)

        right_layout = QVBoxLayout()
        right_layout.addLayout(search_layout)
        self.table = QTableWidget()
        self.table.setColumnCount(7)  # Оновлено на 7 колонок
        self.table.setHorizontalHeaderLabels(
            ["ID", "Назва", "Група", "Податкова ставка", "UKTZED", "Ціна", "Кількість"])
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.cellDoubleClicked.connect(self.open_edit_goods_dialog)

        # Перевірка і створення таблиці
        self.init_db()

        self.load_data()

        right_layout.addWidget(self.table)

        main_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

        self.add_button.clicked.connect(self.open_add_goods_dialog)
        self.reset_search_button.clicked.connect(self.reset_search)
        self.import_button.clicked.connect(self.import_goods)
        self.export_button.clicked.connect(self.export_goods)

        if parent:
            qr = parent.frameGeometry()
            cp = qr.center()
            self.move(cp - self.rect().center())

        # Ініціалізація IEGoods
        self.ie_goods = IEGoods(self)

    def init_db(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(BASE_DIR, 'database.db')

        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()

            # Перевірка існування таблиці
            cursor.execute("""
                SELECT name FROM sqlite_master WHERE type='table' AND name='goods'
            """)
            if cursor.fetchone() is None:
                # Таблиця не існує, створити її
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS goods (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        group_name TEXT,
                        tax INTEGER NOT NULL,
                        UKTZED INTEGER,
                        price REAL NOT NULL,
                        quantity INTEGER
                    )
                """)
                connection.commit()
                print("Таблиця 'goods' успішно створена.")
            else:
                print("Таблиця 'goods' вже існує.")
        except sqlite3.DatabaseError as e:
            QMessageBox.critical(self, "Помилка", f"Помилка при виконанні SQL запиту: {e}")
        finally:
            try:
                connection.close()
            except NameError:
                print("З'єднання з базою даних не було створено.")
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Помилка", f"Помилка при закритті з'єднання з базою даних: {e}")

    def load_data(self, search_query=''):
        try:
            db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database.db')
            with sqlite3.connect(db_path) as connection:
                query = """
                    SELECT id, name, group_name, tax, UKTZED, price, quantity
                    FROM goods
                    WHERE name LIKE ? OR group_name LIKE ? OR UKTZED LIKE ?
                """
                search_query = f'%{search_query}%'
                df = pd.read_sql(query, connection, params=(
                    search_query, search_query, search_query))

                df = df.fillna('')

                self.table.setRowCount(len(df))

                for row_idx, row in df.iterrows():
                    for col_idx, value in enumerate(row):
                        item = QTableWidgetItem(str(value))
                        self.table.setItem(row_idx, col_idx, item)

                self.table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Помилка при завантаженні даних: {e}")

    def open_add_goods_dialog(self):
        dialog = AddGoodsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()

    def search_goods(self):
        search_query = self.search_input.text().strip()
        self.load_data(search_query)

    def reset_search(self):
        self.search_input.clear()
        self.load_data()

    def import_goods(self):
        self.ie_goods.import_goods()

    def export_goods(self):
        self.ie_goods.export_goods()

    def open_edit_goods_dialog(self, row, column):
        goods_id = self.table.item(row, 0).text()
        dialog = EditGoodsDialog(self, goods_id)
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()
