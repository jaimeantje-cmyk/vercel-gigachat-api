# api/index.py

import json
from .gigachat_core import get_token_logic # Импорт логики из соседнего файла

def handler(request):
    """
    Точка входа Vercel. Обрабатывает HTTP-запрос и возвращает ответ в формате Vercel.
    """
    
    try:
        # Запускаем логику скрипта
        token_data = get_token_logic()
        
        # Успешный ответ (код 200 по умолчанию)
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "success",
                "token_response": token_data
            }, ensure_ascii=False)
        }

    except Exception as e:
        # Ответ с явным указанием кода 500
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "error",
                "message": "Ошибка выполнения скрипта.",
                "details": str(e)
            }, ensure_ascii=False)
        }
