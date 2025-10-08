# api/gigachat_core.py

from gigachat import GigaChat

# --- ЖЕСТКО ЗАДАН КЛЮЧ ---
AUTH_CREDENTIALS = "MDE5OWI5ZTQtMDExYy03Mzk5LTk0YjEtMWY0NTFhMjIzN2QwOmM1ZGM0NmRhLTY4N2UtNDhhOS1hZjYwLTUyNGQ1Njk5YTc4YQ=="
# --------------------------

def get_token_logic():
    """
    Выполняет чистую логику GigaChat и возвращает результат или ошибку.
    """
    if not AUTH_CREDENTIALS:
        raise ValueError("AUTH_CREDENTIALS не установлен.")

    giga = GigaChat(credentials=AUTH_CREDENTIALS)
    response = giga.get_token()
    return response.json()
