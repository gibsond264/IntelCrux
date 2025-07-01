# bot/telegram_poster.py

import os
import requests
from logger import setup_logger
from dotenv import load_dotenv

load_dotenv()
log = setup_logger()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def post_to_telegram(text: str, media_path: str = None):
    """
    Posts a message to Telegram via HTTP.
    If media_path is provided and exists, uploads the photo with caption.
    """
    try:
        if media_path and os.path.exists(media_path):
            log.info("📤 Sending photo + caption…")
            with open(media_path, "rb") as img:
                resp = requests.post(
                    f"{API_URL}/sendPhoto",
                    data={
                        "chat_id": CHAT_ID,
                        "caption": text,
                        "parse_mode": "HTML"
                    },
                    files={"photo": img}
                )
        else:
            log.info("📤 Sending text…")
            resp = requests.post(
                f"{API_URL}/sendMessage",
                data={
                    "chat_id": CHAT_ID,
                    "text": text,
                    "parse_mode": "HTML"
                }
            )

        if resp.status_code == 200:
            log.info(f"✅ Telegram API OK: sent to {CHAT_ID}")
        else:
            log.error(f"❌ Telegram API error {resp.status_code}: {resp.text}")

    except Exception as e:
        log.error(f"❌ Exception in post_to_telegram: {e}")
