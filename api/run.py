# api/run.py

import json
import os
from gigachat import GigaChat

# --- ЖЕСТКО ЗАДАН КЛЮЧ ---
AUTH_CREDENTIALS = "MDE5OWI5ZTQtMDExYy03Mzk5LTk0YjEtMWY0NTFhMjIzN2QwOmM1ZGM0NmRhLTY4N2UtNDhhOS1hZjYwLTUyNGQ1Njk5YTc4YQ=="
# --------------------------

def handler(request):
    """
    Vercel ожидает либо словарь/список (для 200 OK), либо специальный
    словарь для управления HTTP-кодом. 
    """
    
    if not AUTH_CREDENTIALS:
        return {
            "statusCode": 500,
            "body": json.dumps({"status": "error", "message": "Ключ отсутствует."})
        }

    try:
        giga = GigaChat(credentials=AUTH_CREDENTIALS)
        response = giga.get_token()
        
        # Успешный ответ (код 200 по умолчанию)
        return {
            "status": "success",
            "token_response": response.json() 
        }

    except Exception as e:
        # Ответ с явным указанием кода 500
        return {
            "statusCode": 500,
            "body": json.dumps({
                "status": "error",
                "message": "Ошибка выполнения скрипта GigaChat.",
                "details": str(e)
            })
        }
