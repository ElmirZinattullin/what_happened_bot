# "WHat happened?" Telegram-bot
## Что делает бот
МОжно использовать бота для ответа на частые вопросы или сбора отзывов.
## Как запустить
### 1. Запуск через Docker
- Скачайте проект
- Установите Docker
- Находясь в директории проекта выполните

```shell
docker build  --tag new_bot . 
```
- Получите token для бота или используйте существующий. 
https://core.telegram.org/bots/features#creating-a-new-bot.
- Запустите докер контейнер использую свой token
```shell
docker run -e BOT_TOKEN="1234565613:BOT1-token-example" --name my_container_for_new_bot medical_bot``1
```
- Используйте команды start stop для запуски и останова контейнера
```shell
docker stop my_container_for_new_bot
docker start my_container_for_new_bot
```

### 2. Запуск в ОС.
- Установите python 3.11
- Установите зависимости 
```shell
    pip install -r requirements.txt
```
- Создайте файл .env по шаблону .env.temp редактируя переменные окружения
- Запустите main.py 
```shell
python what_happened_bot/main.py
```

### Скрытые команды бота
- /register_support - Регистрация чата тех.поддержки куда будут отправляться отзывы и вопросы клиентов
- /chat_id - Узнать id текущего чата

