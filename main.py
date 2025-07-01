# bot/main.py

import os
import schedule
import time
import hashlib

from logger import setup_logger
from liveuamap_scraper import scrape_liveuamap
from summarize import summarize_text
from post_builder import build_post
from telegram_poster import post_to_telegram
from telegram_scraper_sync import scrape_telegram

log = setup_logger()

POSTED_IDS_FILE    = "posted_ids.txt"
POSTED_HASHES_FILE = "posted_hashes.txt"


def load_posted_ids():
    if not os.path.exists(POSTED_IDS_FILE):
        return set()
    with open(POSTED_IDS_FILE) as f:
        return set(line.strip() for line in f)


def save_posted_id(pid: str):
    with open(POSTED_IDS_FILE, "a") as f:
        f.write(pid + "\n")


def load_posted_hashes():
    if not os.path.exists(POSTED_HASHES_FILE):
        return set()
    with open(POSTED_HASHES_FILE) as f:
        return set(line.strip() for line in f)


def save_posted_hash(h: str):
    with open(POSTED_HASHES_FILE, "a") as f:
        f.write(h + "\n")


def job_liveuamap():
    posted_ids    = load_posted_ids()
    posted_hashes = load_posted_hashes()

    for region in ("ukraine", "israel", "iran", "russia", "yemen", "north korea", "europe", "usa", "gaza"):
        headlines = scrape_liveuamap(region)
        if not headlines:
            log.warning(f"⚠️ No LiveUAMap headlines for '{region}'.")
            continue

        for headline in headlines:
            pid = f"lu:{region}:{hashlib.md5(headline.encode()).hexdigest()}"
            if pid in posted_ids:
                continue

            summary = summarize_text(headline)
            if not summary:
                continue

            summary_hash = hashlib.md5(summary.encode("utf-8")).hexdigest()
            if summary_hash in posted_hashes:
                log.info(f"🔁 Skipping duplicate summary from LiveUAMap ({pid})")
                save_posted_id(pid)
                continue

            message = (
                f"<b>{region.title()}</b>\n"
                + build_post(summary, source="LiveUAMap")
            )
            post_to_telegram(message)
            save_posted_id(pid)
            save_posted_hash(summary_hash)
            log.info(f"✅ LiveUAMap posted → {pid}")


def job_telegram():
    posted_ids    = load_posted_ids()
    posted_hashes = load_posted_hashes()

    posts = scrape_telegram()
    if not posts:
        log.warning("⚠️ No Telegram posts.")
        return

    for post in posts:
        pid = f"tg:{post['channel']}:{post['id']}"
        if pid in posted_ids:
            continue

        summary = summarize_text(post["text"])
        if not summary:
            continue

        summary_hash = hashlib.md5(summary.encode("utf-8")).hexdigest()
        if summary_hash in posted_hashes:
            log.info(f"🔁 Skipping duplicate summary from Telegram ({pid})")
            save_posted_id(pid)
            continue

        message = f"<b>{summary}</b>"

        media = post.get("media_path")
        if media:
            exists = os.path.exists(media)
            log.info(f"🖼️ Found media file: {media} (exists={exists})")
        else:
            log.info("ℹ️ No media for this post.")

        post_to_telegram(message, media_path=media)
        save_posted_id(pid)
        save_posted_hash(summary_hash)
        log.info(f"✅ Telegram posted → {pid}")


# Schedule every 5 minutes
schedule.every(5).minutes.do(job_liveuamap)
schedule.every(5).minutes.do(job_telegram)

log.info("✅ Bot running every 5m — Telegram + LiveUAMap.")
while True:
    schedule.run_pending()
    time.sleep(1)
