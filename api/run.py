# api/run.py

import json
import requests
import os
from typing import Dict, Any

# --- ЖЕСТКО ЗАДАН КЛЮЧ ДЛЯ ТЕСТА (Используем его как basic auth) ---
AUTH_CREDENTIALS = "MDE5OWI5ZTQtMDExYy03Mzk5LTk0YjEtMWY0NTFhMjIzN2QwOjQxODkzZjVhLTBlOTMtNDAxOS1hYTRlLWVlMmU4NjlkNmVlOQ=="
# ----------------------------------------------------------------------

# URL для получения токена (стандартный для GigaChat/Sber)
AUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

def handler(request: Dict[str, Any]):
    """
    Vercel Handler. Конструирует и отправляет запрос на получение токена GigaChat.
    """

    if not AUTH_CREDENTIALS:
        return {
            "statusCode": 500,
            "body": json.dumps({"status": "error", "message": "Ключ авторизации отсутствует."})
        }

    try:
        # 1. Формирование заголовков для запроса
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': '26d6006f-6887-4180-873b-e85d19a4e610',  # Произвольный RqUID
            'Authorization': f'Basic {AUTH_CREDENTIALS}'
        }

        # 2. Формирование тела запроса
        payload = {
            'scope': 'GIGACHAT_API_PERS'
        }

        # 3. Выполнение запроса с отключенной проверкой SSL (требуется для Sber API)
        response = requests.post(
            AUTH_URL, 
            headers=headers, 
            data=payload,
            verify=False # Отключаем проверку SSL/TLS, часто требуется для API Сбера
        )
        
        # 4. Проверка HTTP-статуса
        response.raise_for_status() 

        # Успешный ответ (код 200 по умолчанию)
        return {
            "status": "success",
            "token_response": response.json() 
        }

    except requests.exceptions.RequestException as e:
        # Ловим ошибки сети, таймауты или 4xx/5xx от API
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
        # Ловим другие ошибки
        return {
            "statusCode": 500,
            "body": json.dumps({
                "status": "error",
                "message": "Непредвиденная ошибка Vercel.",
                "details": str(e)
            })
        }
