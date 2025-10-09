// api/run.js

// Импортируем 'child_process' для выполнения системных команд
const { exec } = require('child_process');

// Ваш ключ авторизации Basic (тот же самый)
const AUTH_CREDENTIALS = 'Basic MDE5OWI5ZTQtMDExYy03Mzk5LTk0YjEtMWY0NTFhMjIzN2QwOmYyM2JhODg4LTYxNTQtNDU2YS1iNzFhLWFlN2NmNjllNGM3Ng==';

// Функция, которую Vercel будет вызывать при запросе
module.exports = (req, res) => {
    // Проверяем, что запрос пришел методом POST
    if (req.method !== 'POST') {
        res.status(405).send('Method Not Allowed. Use POST.');
        return;
    }

    // Собираем команду curl
    const curlCommand = `
        curl -k -L -X POST 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth' \\
        -H 'Content-Type: application/x-www-form-urlencoded' \\
        -H 'Accept: application/json' \\
        -H 'RqUID: ${Date.now()}' \\
        -H 'Authorization: ${AUTH_CREDENTIALS}' \\
        --data-urlencode 'scope=GIGACHAT_API_PERS'
    `;
    
    // Выполняем команду
    exec(curlCommand, (error, stdout, stderr) => {
        if (error) {
            // Если curl вернул ошибку выполнения (не ошибку HTTP)
            console.error(`exec error: ${error}`);
            res.status(500).json({ 
                status: 'error', 
                message: 'Function execution error', 
                details: stderr || error.message 
            });
            return;
        }

        try {
            // Парсим JSON-ответ от curl
            const tokenResponse = JSON.parse(stdout);

            if (tokenResponse.access_token) {
                // Успешный ответ
                res.status(200).json({
                    status: 'success',
                    token_response: tokenResponse
                });
            } else {
                // Ошибка от GigaChat API (например, неверный ключ)
                res.status(500).json({
                    status: 'error',
                    message: 'GigaChat API returned an error',
                    token_response: tokenResponse
                });
            }

        } catch (e) {
            // Ошибка парсинга JSON
            res.status(500).json({ 
                status: 'error', 
                message: 'Failed to parse cURL output', 
                details: stdout 
            });
        }
    });
};
