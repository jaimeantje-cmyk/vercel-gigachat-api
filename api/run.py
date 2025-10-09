# api/run.py

import json
# Используем относительный импорт, чтобы избежать конфликта
from .core_logic import execute_logic 
from typing import Dict, Any

def handler(request: Dict[str, Any]):
    """
    Основная точка входа Vercel.
    """

    try:
        # Вызываем логику из отдельного файла
        result = execute_logic()
        
        # Успешный ответ
        return result
        
    except Exception as e:
        # Обработка ошибок, включая ошибки HTTP от requests
        error_details = str(e)
        if hasattr(e, 'response') and e.response.text:
             try:
                 error_details = e.response.json()
             except json.JSONDecodeError:
                 error_details = e.response.text
        
        return {
            "statusCode": 500,
            "body": json.dumps({
                "status": "error",
                "message": "Ошибка выполнения скрипта.",
                "details": error_details
            })
        }
