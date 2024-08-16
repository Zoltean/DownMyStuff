import logging
import json
import requests

def get_shift_info(api_url, access_token):
    """Отримання інформації про останню зміну."""
    endpoint = f"{api_url}/api/v1/shifts"
    params = {
        'statuses[]': ['OPENED', 'CLOSED'],  # Включити статуси, які можуть бути актуальними
        'limit': 1,  # Лише одна остання зміна
        'desc': True  # Сортування у зворотному порядку
    }

    headers = {
        'accept': 'application/json',
        'X-Client-Name': 'DownMyStuff',
        'X-Client-Version': 'v0.0.1',
        'Authorization': f'Bearer {access_token}'
    }

    # Логування пейлоаду запиту
    logging.debug(f"Запит до API: {endpoint}")
    logging.debug(f"Заголовки запиту: {headers}")
    logging.debug(f"Параметри запиту: {params}")

    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()  # Перевірка наявності помилок HTTP

        # Логування статусу, заголовків та тексту відповіді
        logging.debug(f"Статус відповіді: {response.status_code}")
        logging.debug(f"Заголовки відповіді: {response.headers}")

        # Перевірка наявності даних у відповіді
        response_text = response.text
        if not response_text.strip():  # Перевірка, чи відповідь не є пустою
            logging.error("Сервер повернув пусту відповідь.")
            raise Exception("Сервер повернув пусту відповідь.")

        logging.debug(f"Відповідь API (текст): {response_text}")

        try:
            shift_data = response.json()  # Спроба перетворення в JSON
        except json.JSONDecodeError:
            logging.error("Відповідь сервера не є правильним JSON.")
            raise Exception("Відповідь сервера не є правильним JSON.")

        if not isinstance(shift_data, dict):
            logging.error("Отримані дані не є правильним JSON-об'єктом.")
            raise Exception("Отримані дані не є правильним JSON-об'єктом.")

        results = shift_data.get('results', [])
        if not results:
            logging.error("Немає результатів у відповіді.")
            raise Exception("Немає результатів у відповіді.")

        # Отримання останньої зміни
        last_shift = results[0]

        status = last_shift.get('status', 'UNKNOWN')
        status_color = {
            'OPENED': '#00FF00',
            'CLOSED': '#008000'
        }.get(status, 'red')

        status_text = {
            'OPENED': 'Відкрита',
            'CLOSED': 'Закрита'
        }.get(status, 'ПОМИЛКА - Спробуйте оновити статус зміни через хвилину, якщо і надалі буде помилка, зверніться до підтримки Чекбокс')

        return {
            'status_text': status_text,
            'status_color': status_color,
            'id': last_shift.get('id', 'N/A'),
            'serial': last_shift.get('serial', 'N/A'),
            'opened_at': last_shift.get('opened_at', 'N/A'),
            'closed_at': last_shift.get('closed_at', 'N/A'),
            'emergency_close': last_shift.get('emergency_close', 'N/A'),
            'emergency_close_details': last_shift.get('emergency_close_details', 'N/A')
        }

    except requests.RequestException as e:
        logging.error(f"Не вдалося здійснити запит: {e}")
        raise Exception(f"Не вдалося здійснити запит: {e}")
