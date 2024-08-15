import logging
import json
import requests

def get_shift_info(api_url, access_token, info_text):
    """Отримання інформації про зміну і оновлення текстового блоку."""
    endpoint = f"{api_url}/api/v1/cashier/shift"

    headers = {
        'accept': 'application/json',
        'X-Client-Name': 'Test-Client-Name',
        'X-Client-Version': 'Test-Client-Version',
        'Authorization': f'Bearer {access_token}'
    }

    # Логування пейлоаду запиту
    logging.debug(f"Запит до API: {endpoint}")
    logging.debug(f"Заголовки запиту: {headers}")

    try:
        response = requests.get(endpoint, headers=headers)
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
            info_text.setHtml("<font color='red'>Наразі інформації про відкриту зміну немає.</font>")
            logging.error("Отримані дані не є правильним JSON-об'єктом")
            return

        status = shift_data.get('status', 'UNKNOWN')
        status_color = {
            'OPENED': 'green',
            'CLOSED': 'yellow'
        }.get(status, 'red')

        status_text = {
            'OPENED': 'Відкрита',
            'CLOSED': 'Закрита'
        }.get(status, 'ПОМИЛКА - зверніться в підтримку Чекбокс')

        info_text.setHtml(f"<b>Статус:</b> <font color='{status_color}'><b>{status_text}</b></font><br>"
                           f"<b>ID:</b> {shift_data.get('id', 'N/A')}<br>"
                           f"<b>Serial:</b> {shift_data.get('serial', 'N/A')}<br>"
                           f"<b>Opened At:</b> {shift_data.get('opened_at', 'N/A')}<br>"
                           f"<b>Closed At:</b> {shift_data.get('closed_at', 'N/A')}<br>"
                           f"<b>Emergency Close:</b> {shift_data.get('emergency_close', 'N/A')}<br>"
                           f"<b>Emergency Close Details:</b> {shift_data.get('emergency_close_details', 'N/A')}<br>")

    except requests.RequestException as e:
        logging.error(f"Не вдалося здійснити запит: {e}")
        info_text.setHtml(f"<font color='red'>Не вдалося здійснити запит: {e}</font>")
