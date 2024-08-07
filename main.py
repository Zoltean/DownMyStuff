import sys
import logging
import os
import datetime
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow


def setup_logging():
    """Налаштування логування для виведення в консоль і запису в файл."""
    # Створення директорії для логів, якщо вона не існує
    log_dir = 'log'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Форматування для логів
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )

    # Унікальне ім'я файлу з датою і часом
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_name = f'app_{current_time}.log'
    log_file_path = os.path.join(log_dir, log_file_name)

    # Налаштування обробника для консолі
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Налаштування обробника для файлу
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setFormatter(formatter)

    # Налаштування кореневого логера
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Видалення старих файлів
    cleanup_old_logs(log_dir)


def cleanup_old_logs(directory, age_days=14):
    """Видалення файлів старше вказаного віку."""
    now = datetime.datetime.now()
    cutoff_time = now - datetime.timedelta(days=age_days)

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_time < cutoff_time:
                try:
                    os.remove(file_path)
                    print(f"Видалено старий файл логування: {filename}")
                except Exception as e:
                    print(f"Не вдалося видалити файл {filename}: {e}")


if __name__ == "__main__":
    setup_logging()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
