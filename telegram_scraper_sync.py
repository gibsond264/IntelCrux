# bot/telegram_scraper_sync.py

import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

from logger import setup_logger

load_dotenv()
log = setup_logger()

API_ID    = int(os.getenv("TELEGRAM_API_ID"))
API_HASH  = os.getenv("TELEGRAM_API_HASH")
CHANNELS  = [
    c.strip()
    for c in os.getenv("TELEGRAM_CHANNELS", "").split(",")
    if c.strip()
]
MEDIA_DIR = os.getenv("TELEGRAM_MEDIA_DIR", "media")

os.makedirs(MEDIA_DIR, exist_ok=True)

def scrape_telegram():
    """
    Synchronously fetch the last 30 minutes of messages from each channel,
    download media if present, and return a list of dicts:
      {
        "id":         <message_id_str>,
        "text":       <message_text>,
        "channel":    <channel_username>,
        "media_path": <local_filepath_or_None>
      }
    """
    client = TelegramClient("intelcrux_session", API_ID, API_HASH)
    client.start()

    cutoff = datetime.now(timezone.utc) - timedelta(minutes=30)
    results = []

    for channel in CHANNELS:
        try:
            entity  = client.get_entity(channel)
            history = client(
                GetHistoryRequest(
                    peer=entity,
                    limit=20,
                    offset_date=None,
                    offset_id=0,
                    max_id=0,
                    min_id=0,
                    add_offset=0,
                    hash=0
                )
            )

            for msg in history.messages:
                # skip empty or too-old
                if not msg.message or msg.date < cutoff:
                    continue

                entry = {
                    "id":         str(msg.id),
                    "text":       msg.message,
                    "channel":    channel,
                    "media_path": None
                }

                if msg.media:
                    try:
                        fn   = f"{channel}_{msg.id}"
                        path = client.download_media(
                            msg.media,
                            file=os.path.join(MEDIA_DIR, fn)
                        )
                        entry["media_path"] = path
                    except Exception as e:
                        log.error(f"Failed to download media {channel}#{msg.id}: {e}")

                results.append(entry)

        except Exception as e:
            log.error(f"Error scraping {channel}: {e}")

    client.disconnect()
    return results
