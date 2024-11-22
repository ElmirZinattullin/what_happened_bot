import os
import sys
from dotenv import find_dotenv, load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
LOG_API_PASSWORD = os.getenv("API_PASSWORD")
LOG_API_URL = os.getenv("LOG_API_URL")
LOG_LEVEL = os.getenv("LOG_LEVEL")
if not BOT_TOKEN:
    print("Переменные окружения не загружены. Отсутствует BOT_TOKEN")
    sys.exit(1)

