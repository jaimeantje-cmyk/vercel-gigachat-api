# api/core_logic.py

import json
import requests

# --- ЖЕСТКО ЗАДАН КЛЮЧ ДЛЯ ТЕСТА ---
AUTH_CREDENTIALS = "MDE5OWI5ZTQtMDExYy03Mzk5LTk0YjEtMWY0NTFhMjIzN2QwOjVlZjk0YzYwLTAzZTUtNDdiNC04MjhmLWNmZWZkNGQ2NDY2NQ=="
# ------------------------------------
AUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

def execute_logic():
    """Отдельная функция, выполняющая весь запрос."""
    
    # 1. Формирование запроса (как в предыдущей версии)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': '26d6006f-6887-4180-873b-e85d19a4e610',
        'Authorization': f'Basic {AUTH_CREDENTIALS}'
    }
    payload = {'scope': 'GIGACHAT_API_PERS'}

    response = requests.post(
        AUTH_URL, 
        headers=headers, 
        data=payload,
        verify=False
    )
    
    response.raise_for_status() 

    return {
        "status": "success",
        "token_response": response.json() 
    }
