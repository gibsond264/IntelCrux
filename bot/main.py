import schedule
import time
from twitter_monitor import get_latest_tweets, post_tweet
from liveuamap_scraper import scrape_liveuamap
from summarize import summarize_text
from logger import setup_logger

log = setup_logger()

def job_twitter():
    log.info("🔁 Running Twitter scan...")
    get_latest_tweets()

def job_liveuamap():
    log.info("🔁 Scraping Liveuamap...")
    for region in ["ukraine", "israel"]:
        headlines = scrape_liveuamap(region)
        for h in headlines:
            summary = summarize_text(h)
            if summary:
                final_post = f"🌍 {summary} (Liveuamap - {region.title()})"
                if len(final_post) <= 280:
                    post_tweet(final_post)

schedule.every(2).minutes.do(job_twitter)
schedule.every(2).minutes.do(job_liveuamap)

log.info("✅ IntelCrux OSINT bot running every 2 minutes.")
while True:
    schedule.run_pending()
    time.sleep(1)
