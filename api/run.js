// api/run.js

// Импортируем 'child_process' для выполнения системных команд
const { exec } = require('child_process');

// Ваш ключ авторизации Basic (тот же самый)
const AUTH_CREDENTIALS = 'Basic MDE5OWI5ZTQtMDExYy03Mzk5LTk0YjEtMWY0NTFhMjIzN2QwOmYyM2JhODg4LTYxNTQtNDU2YS1iNzFhLWFlN2NmNjllNGM3Ng==';

// Функция, которую Vercel будет вызывать при з апросе
module.exports = (req, res) => {
    // Проверяем, что запрос пришел методом POST
    if (req.method !== 'POST') {
        res.status(405).send('Method Not Allowed. Use POST.');
        return;
    }

    // Собираем команду curl
    const curlCommand = `
        curl -L --insecure -X POST 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth' \\
        -H 'Content-Type: application/x-www-form-urlencoded' \\
        -H 'Accept: application/json' \\
        -H 'RqUID: ${Date.now()}' \\
        -H 'Authorization: ${AUTH_CREDENTIALS}' \\
        --data-urlencode 'scope=GIGACHAT_API_PERS'
    `;
    
    // Выполняем команду
    exec(curlCommand, (error, stdout, stderr) => {
    // 1. Проверяем ошибку выполнения команды (если curl не найден или не запустился)
    if (error) {
        console.error(`exec error: ${error}`);
        res.status(500).json({ 
            status: 'error', 
            message: 'Command execution failed (curl not found or failed)', 
            details: stderr || error.message 
        });
        return;
    }

    try {
        // 2. Пытаемся распарсить stdout
        const tokenResponse = JSON.parse(stdout);

        if (tokenResponse.access_token) {
            res.status(200).json({
                status: 'success',
                token_response: tokenResponse
            });
        } else {
            // Ошибка от GigaChat API (например, неверный ключ), но JSON распарсен
            res.status(500).json({
                status: 'error',
                message: 'GigaChat API returned an error',
                token_response: tokenResponse
            });
        }

    } catch (e) {
        // 3. Ошибка парсинга JSON (stdout пустой или не JSON)
        res.status(500).json({ 
            status: 'error', 
            message: 'Failed to parse cURL output (Output was not valid JSON)', 
            details: {
                stdout: stdout.trim() || "Empty or invalid output",
                stderr: stderr.trim() || "No error output (stderr is empty)"
            }
        });
    }
});
};
