# api/run.py

import json
import requests
import os
from typing import Dict, Any

# --- ЖЕСТКО ЗАДАН КЛЮЧ ДЛЯ ТЕСТА ---
AUTH_CREDENTIALS = "MDE5OWI5ZTQtMDExYy03Mzk5LTk0YjEtMWY0NTFhMjIzN2QwOjVlZjk0YzYwLTAzZTUtNDdiNC04MjhmLWNmZWZkNGQ2NDY2NQ=="
# ----------------------------------------------------------------------

AUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

def handler(request: Dict[str, Any]):
    """
    Vercel Handler. Самая простая функция для Vercel.
    """

    if not AUTH_CREDENTIALS:
        return {
            "statusCode": 500,
            "body": json.dumps({"status": "error", "message": "Ключ отсутствует."})
        }

    try:
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
            verify=False # Отключаем проверку SSL, т.к. может потребоваться для Сбера
        )
        
        response.raise_for_status() 

        # Успешный ответ (код 200 по умолчанию)
        return {
            "status": "success",
            "token_response": response.json() 
        }

    except requests.exceptions.RequestException as e:
        # Ловим ошибки HTTP (4xx, 5xx)
        error_details = response.json() if 'response' in locals() and response.text else str(e)
        return {
            "statusCode": 500,
            "body": json.dumps({
                "status": "error",
                "message": "Ошибка запроса к GigaChat API.",
                "details": error_details
            })
        }
    except Exception as e:
        # Ловим непредвиденные ошибки
        return {
            "statusCode": 500,
            "body": json.dumps({
                "status": "error",
                "message": "Непредвиденная ошибка Vercel.",
                "details": str(e)
            })
        }
