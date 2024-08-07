import hashlib
from datetime import datetime, timedelta

def generate_license_key(device_id, months):
    """Генерує ліцензійний ключ на основі DEVICE_ID та терміна ліцензії."""
    expiration_date = datetime.now() + timedelta(days=31 * months)
    raw_key = f"{device_id}-{expiration_date.strftime('%Y-%m-%d')}-{months}"
    license_key = hashlib.sha256(raw_key.encode()).hexdigest()
    return license_key

def verify_license_key(device_id, license_key, months):
    """Перевіряє ліцензійний ключ на основі DEVICE_ID та терміна ліцензії."""
    expiration_date = datetime.now() + timedelta(days=31 * months)
    raw_key = f"{device_id}-{expiration_date.strftime('%Y-%m-%d')}-{months}"
    expected_key = hashlib.sha256(raw_key.encode()).hexdigest()
    return expected_key == license_key

def main():
    while True:
        device_id = input("Введіть DEVICE_ID (або 'exit' для виходу): ")
        if device_id.lower() == 'exit':
            break

        try:
            months = int(input("Введіть термін ліцензії в місяцях: "))
            if months <= 0:
                print("Кількість місяців повинна бути додатною.")
                continue

            # Генерація ключа
            license_key = generate_license_key(device_id, months)
            print(f"Сгенерований ключ ліцензії на {months} місяців: {license_key}")

            # Перевірка ключа
            is_valid = verify_license_key(device_id, license_key, months)
            print(f"Чи є ключ ліцензії дійсним: {is_valid}")

        except ValueError:
            print("Будь ласка, введіть коректне число для терміну ліцензії.")

if __name__ == "__main__":
    main()
