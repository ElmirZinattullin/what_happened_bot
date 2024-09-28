import os
from dotenv import find_dotenv, load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print("Переменные окружения не загружены")
