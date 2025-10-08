# api/index.py

import json
from flask import Flask, jsonify, request
from gigachat import GigaChat

# --- Инициализация Flask ---
# Vercel будет искать именно этот экземпляр 'app'
app = Flask(__name__)

# --- ЖЕСТКО ЗАДАН КЛЮЧ ДЛЯ ТЕСТА ---
AUTH_CREDENTIALS = "MDE5OWI5ZTQtMDExYy03Mzk5LTk0YjEtMWY0NTFhMjIzN2QwOmM1ZGM0NmRhLTY4N2UtNDhhOS1hZjYwLTUyNGQ1Njk5YTc4YQ=="
# ------------------------------------

# Определяем маршрут для POST-запроса
@app.route("/api/run", methods=["POST"])
def get_gigachat_token():
    """
    Запускает скрипт GigaChat, используя Flask.
    """
    
    # 1. Проверка ключа
    if not AUTH_CREDENTIALS:
        # Flask возвращает JSON-ответ и код ошибки
        return jsonify(
            {"status": "error", "message": "Ошибка конфигурации: Ключ отсутствует."}
        ), 500

    # 2. Инициализация и выполнение логики GigaChat
    try:
        giga = GigaChat(credentials=AUTH_CREDENTIALS)
        response = giga.get_token()
        
        # Успешный ответ (200 OK)
        return jsonify({
            "status": "success",
            "token_response": response.json() 
        }), 200

    except Exception as e:
        # Ловим и возвращаем ошибку GigaChat
        return jsonify({
            "status": "error",
            "message": "Ошибка выполнения скрипта GigaChat.",
            "details": str(e)
        }), 500

# ВАЖНО: Если вы используете Flask, вам не нужен vercel.json!
# Но так как он уже есть, мы его просто обновим.
