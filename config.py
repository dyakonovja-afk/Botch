import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# лимиты бесплатной версии
FREE_RETURNS = 3
FREE_FILTERS = 3

# таймер диалога (сек)
DIALOG_TIMEOUT = 600  # 10 минут
WARNING_BEFORE_END = 120  # предупреждение за 2 минуты
