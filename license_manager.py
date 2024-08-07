import hashlib
import platform
import socket
import uuid
import sqlite3
import os
from datetime import datetime, timedelta
from cryptography.fernet import Fernet

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'database.db')
SECRET_KEY = b'qj1rGqey6foPfSIwIJB-5WDF4uUE_VjEEzA5Mo7MY84='  # Заміни на свій секретний ключ
cipher_suite = Fernet(SECRET_KEY)

def get_device_id():
    """Генерує унікальний DEVICE_ID на основі різних параметрів системи."""
    system_info = f"{platform.node()}-{uuid.getnode()}-{socket.gethostname()}"
    device_id = hashlib.sha256(system_info.encode()).hexdigest()
    return device_id

def initialize_db():
    """Ініціалізація бази даних."""
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS licenses (
        id INTEGER PRIMARY KEY,
        device_id TEXT NOT NULL,
        license_key TEXT NOT NULL,
        activation_date TEXT NOT NULL,
        expiration_date TEXT NOT NULL,
        UNIQUE(device_id, license_key)
    )
    ''')
    conn.commit()
    conn.close()

def save_license(device_id, license_key, expiry_date):
    """Збереження ліцензії в базі даних."""
    activation_date = datetime.now().strftime('%Y-%m-%d')
    encrypted_expiry_date = cipher_suite.encrypt(expiry_date.strftime('%Y-%m-%d').encode()).decode()
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO licenses (device_id, license_key, activation_date, expiration_date)
    VALUES (?, ?, ?, ?)
    ''', (device_id, license_key, activation_date, encrypted_expiry_date))
    conn.commit()
    conn.close()

def get_license(device_id):
    """Отримання ліцензії з бази даних."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM licenses WHERE device_id = ?', (device_id,))
    license = cursor.fetchone()
    conn.close()
    if license:
        try:
            decrypted_expiry_date = cipher_suite.decrypt(license[4].encode()).decode()
            print(f"Decrypted Expiry Date: {decrypted_expiry_date}")  # Додано для відлагодження
            return license[:4] + (decrypted_expiry_date,)
        except Exception as e:
            print(f"Помилка розшифрування: {e}")
            return None
    return license

def verify_license_key(device_id, license_key, months):
    """Перевіряє ліцензійний ключ на основі DEVICE_ID та терміна ліцензії."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT license_key FROM licenses WHERE device_id = ?', (device_id,))
    existing_license = cursor.fetchone()
    conn.close()

    if existing_license:
        if existing_license[0] == license_key:
            return False  # Ключ вже використовується

    expiration_date = datetime.now() + timedelta(days=31 * months)
    raw_key = f"{device_id}-{expiration_date.strftime('%Y-%m-%d')}-{months}"
    expected_key = hashlib.sha256(raw_key.encode()).hexdigest()

    print(f"Expected Key: {expected_key}, Provided Key: {license_key}")
    return expected_key == license_key

def activate_license_key(device_id, license_key, months):
    """Активує новий ліцензійний ключ і оновлює строк дії в базі даних."""
    if verify_license_key(device_id, license_key, months) is False:
        return False  # Ліцензійний ключ вже використовується або неправильний

    activation_date = datetime.now()
    new_expiration_date = activation_date + timedelta(days=31 * months)
    encrypted_expiration_date = cipher_suite.encrypt(new_expiration_date.strftime('%Y-%m-%d').encode()).decode()

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Отримання існуючих ліцензій
    cursor.execute('SELECT expiration_date FROM licenses WHERE device_id = ?', (device_id,))
    existing_license = cursor.fetchone()

    if existing_license:
        try:
            # Існуюча дата закінчення терміну
            existing_expiration_date = datetime.strptime(
                cipher_suite.decrypt(existing_license[0].encode()).decode(), '%Y-%m-%d')
            # Розрахунок нової дати закінчення терміну
            new_expiration_date = max(existing_expiration_date, activation_date) + timedelta(days=31 * months)
            encrypted_expiration_date = cipher_suite.encrypt(new_expiration_date.strftime('%Y-%m-%d').encode()).decode()
        except Exception as e:
            print(f"Помилка розшифрування існуючої дати закінчення терміну: {e}")

    # Збереження нової ліцензії
    print(
        f"Saving License: Device ID: {device_id}, Key: {license_key}, Activation Date: {activation_date.strftime('%Y-%m-%d')}, Expiration Date: {new_expiration_date.strftime('%Y-%m-%d')}")
    cursor.execute('''
    INSERT OR REPLACE INTO licenses (device_id, license_key, activation_date, expiration_date)
    VALUES (?, ?, ?, ?)
    ''', (device_id, license_key, activation_date.strftime('%Y-%m-%d'),
          encrypted_expiration_date))

    conn.commit()
    conn.close()
    return True

def check_license():
    """Перевіряє стан ліцензії з бази даних."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    device_id = get_device_id()
    cursor.execute('SELECT expiration_date FROM licenses WHERE device_id = ?', (device_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        try:
            expiration_date = datetime.strptime(cipher_suite.decrypt(row[0].encode()).decode(), '%Y-%m-%d')
            print(f"Expiration Date: {expiration_date}")  # Додано для відлагодження
            if datetime.now() < expiration_date:
                return True
        except Exception as e:
            print(f"Помилка розшифрування: {e}")
    return False

# Ініціалізація бази даних при імпорті модуля
initialize_db()
