# api/run.py

import json
import requests
import os
from typing import Dict, Any

# --- ЖЕСТКО ЗАДАН КЛЮЧ ДЛЯ ТЕСТА (BASE64) ---
# В реальном проекте используйте os.environ.get("GIGACHAT_CREDENTIALS")
AUTH_CREDENTIALS = "MDE5OWI5ZTQtMDExYy03Mzk5LTk0YjEtMWY0NTFhMjIzN2QwOmQwZTk2YWU1LWZmY2YtNGQ4Ny05MzhmLTMyZmM0N2I4YzdmNg=="
# ----------------------------------------------------------------------

# URL для получения токена GigaChat
AUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

def handler(request: Dict[str, Any]):
    """
    Основная функция, которую вызывает Vercel (точка входа).
    Она отправляет прямой POST-запрос на GigaChat API.
    """

    if not AUTH_CREDENTIALS:
        return {
            "statusCode": 500,
            "body": json.dumps({"status": "error", "message": "Ключ авторизации отсутствует."})
        }

    try:
        # 1. Формирование заголовков для Basic-авторизации
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': '26d6006f-6887-4180-873b-e85d19a4e610',  # Произвольный, но уникальный ID
            'Authorization': f'Basic {AUTH_CREDENTIALS}'
        }

        # 2. Формирование тела запроса
        payload = {
            'scope': 'GIGACHAT_API_PERS'
        }

        # 3. Выполнение запроса
        # verify=False часто требуется для доступа к API Сбера
        response = requests.post(
            AUTH_URL, 
            headers=headers, 
            data=payload,
            verify=False 
        )
        
        # Вызовет исключение, если HTTP-статус 4xx или 5xx
        response.raise_for_status() 

        # Успешный ответ (Vercel вернет 200 OK)
        return {
            "status": "success",
            "token_response": response.json() 
        }

    except requests.exceptions.RequestException as e:
        # Ловим ошибки HTTP (4xx, 5xx), сети или таймауты
        
        # Пытаемся получить тело ошибки, если запрос дошел до сервера
        error_details = "Network or connection error."
        if 'response' in locals():
             try:
                 error_details = response.json()
             except json.JSONDecodeError:
                 error_details = response.text
        
        return {
            "statusCode": response.status_code if 'response' in locals() else 500,
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
