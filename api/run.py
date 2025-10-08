# api/run.py

import json
import os
from gigachat import GigaChat
from typing import Dict, Any

# --- ВНИМАНИЕ: ЖЕСТКО ЗАДАН КЛЮЧ ДЛЯ ТЕСТА ---
AUTH_CREDENTIALS = "MDE5OWI5ZTQtMDExYy03Mzk5LTk0YjEtMWY0NTFhMjIzN2QwOmM1ZGM0NmRhLTY4N2UtNDhhOS1hZjYwLTUyNGQ1Njk5YTc4YQ=="
# ----------------------------------------------------

def handler(request: Dict[str, Any]):
    """
    Основная функция, которую вызывает Vercel. 
    Она должна возвращать либо словарь/список (для JSON), либо строку.
    """
    
    # 1. Проверка наличия ключа
    if not AUTH_CREDENTIALS:
        # В случае ошибки возвращаем словарь с кодом 500
        return {
            "statusCode": 500,
            "body": {"status": "error", "message": "Ошибка конфигурации: Ключ отсутствует."}
        }

    # 2. Инициализация и выполнение логики GigaChat
    try:
        giga = GigaChat(credentials=AUTH_CREDENTIALS)
        response = giga.get_token()
        
        # Успешный ответ: возвращаем словарь. Vercel сам добавит статус 200 и Content-Type: application/json
        return {
            "status": "success",
            "token_response": response.json() 
        }

    except Exception as e:
        # В случае ошибки API GigaChat, возвращаем словарь с кодом 500
        return {
            "statusCode": 500,
            "body": {
                "status": "error",
                "message": "Ошибка выполнения скрипта GigaChat.",
                "details": str(e)
            }
        }

