import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

from logger import setup_logger

load_dotenv()
log = setup_logger()

API_ID    = int(os.getenv("TELEGRAM_API_ID"))
API_HASH  = os.getenv("TELEGRAM_API_HASH")
CHANNELS  = [c.strip() for c in os.getenv("TELEGRAM_CHANNELS", "").split(",") if c.strip()]
MEDIA_DIR = os.getenv("TELEGRAM_MEDIA_DIR", "media")

# Ensure media directory exists
os.makedirs(MEDIA_DIR, exist_ok=True)

client = TelegramClient("intelcrux_session", API_ID, API_HASH)

async def scrape_telegram():
    """
    Fetch the last 30 minutes of messages from each configured
    Telegram channel, download any media, and return a list of dicts:
      {
        "id":        <message_id_as_str>,
        "text":      <message_text>,
        "channel":   <channel_username>,
        "media_path":<local_filepath_or_None>
      }
    """
    await client.start()
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=30)
    results = []

    for channel in CHANNELS:
        try:
            entity = await client.get_entity(channel)
            history = await client(GetHistoryRequest(
                peer=entity,
                limit=20,
                offset_date=None,
                offset_id=0,
                max_id=0,
                min_id=0,
                add_offset=0,
                hash=0
            ))

            for msg in history.messages:
                # skip empty or too-old messages
                if not msg.message or msg.date < cutoff:
                    continue

                entry = {
                    "id":        str(msg.id),
                    "text":      msg.message,
                    "channel":   channel,
                    "media_path": None
                }

                # download any media (photo, docs, etc.)
                if msg.media:
                    try:
                        filename = f"{channel}_{msg.id}"
                        path = await msg.download_media(
                            file=os.path.join(MEDIA_DIR, filename)
                        )
                        entry["media_path"] = path
                    except Exception as e:
                        log.error(f"Failed to download media {channel}#{msg.id}: {e}")

                results.append(entry)

        except Exception as e:
            log.error(f"Error scraping {channel}: {e}")

    await client.disconnect()
    return results
