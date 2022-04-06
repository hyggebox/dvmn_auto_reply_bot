# Бот-автоответчик для Telegram и ВК

Бот распознаёт стандартные реплики пользователей с помощью технологии 
[DialogFlow](https://dialogflow.cloud.google.com/#/login) (облачный сервис 
распознавания естественного языка от Google) и даёт на них ответы.

Для работы бота необходимо создать аккаунт DialogFlow и 
[проект](https://cloud.google.com/dialogflow/es/docs/quick/setup) в нём.


## Требования

- Для запуска вам понадобится Python 3.6 или выше.
- Токен телеграм-бота (создайте бота через диалог с ботом 
[@BotFather](https://telegram.me/BotFather) и получите токен) 


## Переменные окружения

<table>
<tr>
<td>Переменная</td>
<td>Тип данных</td>
<td>Значение</td>
</tr>
<tr>
<td>PROJECT_ID</td>
<td>str</td>
<td>ID проекта DialogFlow</td>
</tr>
<tr>
<td>GOOGLE_APPLICATION_CREDENTIALS</td>
<td>путь к файлу</td>
<td>Путь к JSON-ключу ( <a href="https://cloud.google.com/docs/authentication/getting-started" target="_blank">подробнее</a> )</td>
</tr>
<tr>
<td>VK_TOKEN</td>
<td>str</td>
<td>Ключ доступа вашего сообщества ВК</td>
</tr>
<tr>
<td>VK_ADMIN_USER_ID</td>
<td>str</td>
<td>user id администратора сообщества (этому пользователю будут приходить логи бота)</td>
</tr>
<tr>
<td>TG_BOT_TOKEN</td>
<td>str</td>
<td>Токен Телеграм-бота</td>
</tr>
<tr>
<td>TG_ADMIN_CHAT_ID</td>
<td>str</td>
<td>ID администратора в Телеграм (этому пользователю будут приходить логи бота)</td>
</tr>
</table>


## Установка

- Загрузите код из репозитория
- Создайте файл `.env` в корневой папке и пропишите переменные окружения 
в формате: `ПЕРЕМЕННАЯ=значение`

- Установите зависимости командой:
```shell
pip install -r requirements.txt
```


### Обучение бота

Для автоматического обучения бота необходимо создать файл `training_phrases.json` 
в корне проекта с примерными вопросами и ответами на эти вопросы следующего вида:
```json
{
  "Тема 1": {
    "questions": [
      "Текст вопроса 1",
      "Текст вопроса 2",
      "Текст вопроса 3",
      "Текст вопроса 4"
    ],
    "answer": "Текст ответа"
  },
  "Тема 2": {
    "questions": [
      "Текст вопроса 1",
      "Текст вопроса 2",
      "Текст вопроса 3"
    ],
    "answer": "Текст ответа"
  },
}
```

- Запустите тренировку бота командой:
```commandline
python bot_training.py
```


### Запуск бота

Зарпустите ботов командами:
```commandline
python tg_bot.py
python vk_bot.py
```
