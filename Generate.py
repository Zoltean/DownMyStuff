import hashlib
from datetime import datetime, timedelta

def generate_license_key(device_id, months):
    """Генерує ліцензійний ключ на основі DEVICE_ID та терміна ліцензії."""
    expiration_date = datetime.now() + timedelta(days=30 * months)
    raw_key = f"{device_id}-{expiration_date.strftime('%Y-%m-%d')}-{months}"
    license_key = hashlib.sha256(raw_key.encode()).hexdigest()
    return license_key

def verify_license_key(device_id, license_key, months):
    """Перевіряє ліцензійний ключ на основі DEVICE_ID та терміна ліцензії."""
    expiration_date = datetime.now() + timedelta(days=31 * months)
    raw_key = f"{device_id}-{expiration_date.strftime('%Y-%m-%d')}-{months}"
    expected_key = hashlib.sha256(raw_key.encode()).hexdigest()
    return expected_key == license_key

device_id = 'a67ebf539c2769eaa094f462c71b38c0b439bf33d11d157a8a225d50696882a6'  # `device_id`, який надав клієнт
months = 1  # Термін ліцензії в місяцях

# Генерація ключа
license_key = generate_license_key(device_id, months)
print(f"Generated License Key for {months} months: {license_key}")

# Перевірка ключа
is_valid = verify_license_key(device_id, license_key, months)
print(f"Is License Key Valid: {is_valid}")
