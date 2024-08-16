import requests

# Глобальні змінні для кешування
cached_shift_data = None
cached_shift_id = None

def create_shift(api_url, access_token, license_key):
    """Створює нову зміну"""
    global cached_shift_data
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Client-Name': 'DownMyStuff',
        'X-Client-Version': 'v0.0.1',
        'X-License-Key': license_key,
    }
    payload = {}

    response = requests.post(f'{api_url}/api/v1/shifts', headers=headers, json=payload)
    if response.status_code == 202:
        cached_shift_data = response.json()
        return cached_shift_data.get('id')
    else:
        raise Exception(f"Не вдалося створити зміну: {response.text}")

def close_shift(api_url, access_token, shift_id, license_key):
    """Закриває зміну"""
    global cached_shift_data
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Client-Name': 'DownMyStuff',
        'X-Client-Version': 'v0.0.1',
        'X-License-Key': license_key,
    }
    payload = {
        'skip_client_name_check': False
    }

    response = requests.post(f'{api_url}/api/v1/shifts/{shift_id}/close', headers=headers, json=payload)
    if response.status_code == 202:
        # Очистка кешованих даних
        cached_shift_data = None
        global cached_shift_id
        cached_shift_id = None
        return shift_id
    else:
        raise Exception(f"Не вдалося закрити зміну: {response.text}")

def check_shift_status(api_url, access_token, shift_id):
    """Перевіряє статус зміни"""
    global cached_shift_data
    if cached_shift_data and cached_shift_data.get('id') == shift_id:
        return cached_shift_data.get('status')

    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Client-Name': 'DownMyStuff',
        'X-Client-Version': 'v0.0.1',
    }

    response = requests.get(f'{api_url}/api/v1/shifts/{shift_id}', headers=headers)
    if response.status_code == 200:
        cached_shift_data = response.json()
        return cached_shift_data.get('status')
    else:
        raise Exception(f"Помилка перевірки статусу зміни: {response.text}")

def get_current_shift_id(api_url, access_token):
    """Отримує ID поточної зміни"""
    global cached_shift_id
    if cached_shift_id:
        return cached_shift_id

    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Client-Name': 'DownMyStuff',
        'X-Client-Version': 'v0.0.1',
    }

    response = requests.get(f'{api_url}/api/v1/cashier/shift', headers=headers)
    if response.status_code == 200:
        shift_data = response.json()
        if shift_data:
            shift_id = shift_data.get('id')
            if shift_id:
                cached_shift_id = shift_id
                return shift_id
            else:
                raise Exception("ID поточної зміни не знайдено в даних.")
        else:
            raise Exception("Отримані дані від API є порожніми.")
    elif response.status_code == 404:
        raise Exception("Поточну зміну не знайдено. Можливо, вона вже закрита.")
    else:
        raise Exception(f"Не вдалося знайти поточну зміну: {response.text}")
