import hashlib
import platform
import socket
import uuid
import sqlite3
from datetime import datetime, timedelta

from license_manager import generate_license_key

def generate_license_key(device_id, months):
    """Генерує ліцензійний ключ на основі DEVICE_ID та поточного місяця."""
    current_date = datetime.now()
    combined = f"{device_id}-{current_date.strftime('%Y%m')}-{months}"
    license_key = hashlib.sha256(combined.encode()).hexdigest()
    return license_key

device_id = 'device_id_from_client'  # `device_id`, який надав клієнт
months = 1  # Термін ліцензії в місяцях

license_key = generate_license_key(device_id, months)
print(f"Generated License Key for {months} months: {license_key}")
