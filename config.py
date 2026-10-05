import os
import sys
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

def check_token():
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        print("\n" + "="*60)
        print("❌ XATOLIK: Telegram Bot Token topilmadi!")
        print("Iltimos, .env faylini oching va BOT_TOKEN ga Telegram @BotFather bergan tokenni yozing.")
        print("Misol uchun: BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ")
        print("="*60 + "\n")
        sys.exit(1)
