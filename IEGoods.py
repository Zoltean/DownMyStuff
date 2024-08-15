import sqlite3
import pandas as pd
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import os

class IEGoods:
    def __init__(self, parent=None):
        self.parent = parent
        # Змінений шлях до бази даних на кореневу директорію
        self.db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')

    def import_goods(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self.parent, "Імпортувати з Excel", "",
                                                   "Excel Files (*.xlsx);;All Files (*)", options=options)
        if file_name:
            try:
                df = pd.read_excel(file_name)

                # Перевірка наявності обов'язкових стовпців
                required_columns = ['Назва', 'Податкова ставка', 'Ціна']
                missing_columns = [col for col in required_columns if col not in df.columns]
                if missing_columns:
                    QMessageBox.warning(self.parent, "Помилка валідації",
                                        f"Файл містить помилки: Відсутні стовпці: {', '.join(missing_columns)}. Імпорт скасовано.")
                    return

                # Валідація даних
                df.rename(columns={
                    'Назва': 'name',
                    'Група': 'group_name',
                    'Податкова ставка': 'tax',
                    'UKTZED': 'UKTZED',
                    'Ціна': 'price',
                    'Кількість': 'quantity'
                }, inplace=True)

                # Конвертація `UKTZED` і `tax` в int
                if 'UKTZED' in df.columns:
                    df['UKTZED'] = pd.to_numeric(df['UKTZED'], errors='coerce').fillna(0).astype(int)

                if 'tax' in df.columns:
                    df['tax'] = pd.to_numeric(df['tax'], errors='coerce').fillna(0).astype(int)

                # Видалення стовпця 'id', якщо існує
                if 'id' in df.columns:
                    df.drop(columns=['id'], inplace=True)

                # Переконайтеся, що price конвертується в float
                if 'price' in df.columns:
                    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0).astype(float)

                with sqlite3.connect(self.db_path) as connection:
                    df.to_sql('goods', connection, if_exists='append', index=False, method='multi')

                if self.parent:
                    self.parent.load_data()
                QMessageBox.information(self.parent, "Успіх", "Товари успішно імпортовані.")
            except Exception as e:
                QMessageBox.critical(self.parent, "Помилка", f"Помилка імпорту: {e}")

    def export_goods(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self.parent, "Експортувати в Excel", "",
                                                   "Excel Files (*.xlsx);;All Files (*)", options=options)
        if file_name:
            try:
                with sqlite3.connect(self.db_path) as connection:
                    df = pd.read_sql("SELECT name, group_name, tax, UKTZED, price, quantity FROM goods",
                                     connection)
                    df.rename(columns={
                        'name': 'Назва',
                        'group_name': 'Група',
                        'tax': 'Податкова ставка',
                        'UKTZED': 'UKTZED',
                        'price': 'Ціна',
                        'quantity': 'Кількість'
                    }, inplace=True)
                    # Переконайтесь, що `UKTZED` і `tax` є цілими числами
                    df['UKTZED'] = df['UKTZED'].astype(int)
                    df['Податкова ставка'] = df['Податкова ставка'].astype(int)
                    df.to_excel(file_name, index=False)
                QMessageBox.information(self.parent, "Успіх", "Товари успішно експортовані.")
            except Exception as e:
                QMessageBox.critical(self.parent, "Помилка", f"Помилка експорту: {e}")
