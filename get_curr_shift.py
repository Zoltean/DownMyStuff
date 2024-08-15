import logging
import json
import requests

def get_shift_info(api_url, access_token, info_text):
    """Отримання інформації про останню зміну і оновлення текстового блоку."""
    endpoint = f"{api_url}/api/v1/shifts"
    params = {
        'statuses[]': ['OPENED', 'CLOSED'],  # Включити статуси, які можуть бути актуальними
        'limit': 1,  # Лише одна остання зміна
        'desc': True  # Сортування у зворотному порядку
    }

    headers = {
        'accept': 'application/json',
        'X-Client-Name': 'Test-Client-Name',
        'X-Client-Version': 'Test-Client-Version',
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
            info_text.setHtml("<font color='red'>Сервер повернув пусту відповідь.</font>")
            logging.error("Сервер повернув пусту відповідь.")
            return

        logging.debug(f"Відповідь API (текст): {response_text}")

        try:
            shift_data = response.json()  # Спроба перетворення в JSON
        except json.JSONDecodeError:
            info_text.setHtml("<font color='red'>Відповідь сервера не є правильним JSON.</font>")
            logging.error("Відповідь сервера не є правильним JSON.")
            return

        if not isinstance(shift_data, dict):
            info_text.setHtml("<font color='red'>Наразі інформації про зміни немає.</font>")
            logging.error("Отримані дані не є правильним JSON-об'єктом")
            return

        results = shift_data.get('results', [])
        if not results:
            info_text.setHtml("<font color='red'>Наразі інформації про зміни немає.</font>")
            logging.error("Немає результатів у відповіді")
            return

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
        }.get(status, 'ПОМИЛКА - зверніться в підтримку Чекбокс')

        info_text.setHtml(f"<b>Статус:</b> <font color='{status_color}'><b>{status_text}</b></font><br>"
                           f"<b>ID:</b> {last_shift.get('id', 'N/A')}<br>"
                           f"<b>Serial:</b> {last_shift.get('serial', 'N/A')}<br>"
                           f"<b>Відкриття:</b> {last_shift.get('opened_at', 'N/A')}<br>"
                           f"<b>Закриття:</b> {last_shift.get('closed_at', 'N/A')}<br>"
                           f"<b>Аварійне закриття:</b> {last_shift.get('emergency_close', 'N/A')}<br>"
                           f"<b>Деталі аварійного закриття:</b> {last_shift.get('emergency_close_details', 'N/A')}<br>")

    except requests.RequestException as e:
        logging.error(f"Не вдалося здійснити запит: {e}")
        info_text.setHtml(f"<font color='red'>Не вдалося здійснити запит: {e}</font>")
