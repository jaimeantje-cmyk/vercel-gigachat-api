import json
import os
from gigachat import GigaChat
from werkzeug.wrappers import Response # <- Важный импорт для Vercel
from typing import Dict, Any

# --- ВНИМАНИЕ: ЖЕСТКО ЗАДАН КЛЮЧ ДЛЯ ТЕСТА ---
AUTH_CREDENTIALS = "MDE5OWI5ZTQtMDExYy03Mzk5LTk0YjEtMWY0NTFhMjIzN2QwOjVlZjk0YzYwLTAzZTUtNDdiNC04MjhmLWNmZWZkNGQ2NDY2NQ=="
# ----------------------------------------------------

def create_response(status_code: int, data_dict: Dict[str, Any]) -> Response:
    """
    Создает корректный объект Response, используя Werkzeug.
    """
    return Response(
        response=json.dumps(data_dict, ensure_ascii=False),
        status=status_code,
        mimetype="application/json"
    )

def handler(request):
    """
    Основная функция, которую будет вызывать Vercel.
    Именно эта функция (handler) должна быть экспортирована в чистом Python.
    """
    
    # 1. Проверка наличия ключа
    if not AUTH_CREDENTIALS:
        error = {"status": "error", "message": "Ошибка конфигурации: Ключ авторизации отсутствует."}
        return create_response(500, error)

    # 2. Инициализация и выполнение логики GigaChat
    try:
        # Инициализация клиента
        giga = GigaChat(credentials=AUTH_CREDENTIALS)
        
        # Получение токена (логика вашего скрипта)
        response = giga.get_token()
        
        # Подготовка успешного ответа
        result_data = {
            "status": "success",
            "token_response": response.json() 
        }
        
        return create_response(200, result_data)

    except Exception as e:
        # Обработка ошибок GigaChat API
        error_response = {
            "status": "error",
            "message": "Ошибка выполнения скрипта GigaChat.",
            "details": str(e)
        }
        return create_response(500, error_response)

# ВАЖНО: Никакого if __name__ == "__main__": не требуется.
# Vercel ищет функцию 'handler'