import os
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TELEGRAM_BOT_TOKEN")
chat  = os.getenv("TELEGRAM_CHAT_ID")
print("Token:", token)
print("Chat ID:", chat)

bot = Bot(token=token)
try:
    res = bot.send_message(chat_id=chat, text="✅ If you see this, Telegram is working!")
    print("Success:", res)
except Exception as e:
    print("Error sending test message:", e)
