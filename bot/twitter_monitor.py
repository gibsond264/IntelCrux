import os
import time
from datetime import datetime, timedelta
from dateutil import parser as date_parser
from dotenv import load_dotenv
import tweepy

from logger import setup_logger
from summarize import summarize_text
from nitter_scraper import scrape_all_nitter_users

log = setup_logger()

load_dotenv()

# Posting via v1.1 API
auth = tweepy.OAuth1UserHandler(
    os.getenv("TWITTER_API_KEY"),
    os.getenv("TWITTER_API_SECRET"),
    os.getenv("TWITTER_ACCESS_TOKEN"),
    os.getenv("TWITTER_ACCESS_SECRET")
)
api = tweepy.API(auth)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTED_IDS_FILE = os.path.join(BASE_DIR, "posted_ids.txt")

def load_posted_ids():
    if not os.path.exists(POSTED_IDS_FILE):
        return set()
    with open(POSTED_IDS_FILE, "r") as f:
        return set(line.strip() for line in f)

def save_posted_id(tweet_id):
    with open(POSTED_IDS_FILE, "a") as f:
        f.write(f"{tweet_id}\n")

def is_relevant(text):
    keywords = [
        "missile", "airstrike", "strike", "IDF", "mobilization", "air raid",
        "explosion", "explosions", "rocket", "drone", "nuclear", "counteroffensive",
        "invasion", "warplane", "ballistic", "intercept", "mobilized", "military", "border"
    ]
    return any(kw.lower() in text.lower() for kw in keywords)

def post_tweet(text):
    try:
        api.update_status(status=text)
        log.info(f"✅ Posted: {text[:60]}...")
    except Exception as e:
        log.error(f"❌ Error posting: {e}")

def get_latest_tweets():
    tweets = scrape_all_nitter_users()
    posted_ids = load_posted_ids()
    time_threshold = datetime.now() - timedelta(minutes=15)

    for tweet in tweets:
        tweet_id = f"{tweet['username']}_{tweet['timestamp']}"

        # Parse timestamp
        try:
            created_at = date_parser.parse(tweet['timestamp'])
        except Exception:
            log.warning(f"⚠️ Could not parse timestamp for @{tweet['username']}")
            continue

        if created_at < time_threshold:
            log.info(f"⏰ Skipped old tweet from @{tweet['username']} ({tweet['timestamp']})")
            continue

        if tweet_id in posted_ids:
            log.info(f"⏩ Skipped duplicate from @{tweet['username']} at {tweet['timestamp']}")
            continue

        if is_relevant(tweet['text']):
            log.info(f"[RELEVANT] @{tweet['username']}: {tweet['text'][:100]}...")
            summary = summarize_text(tweet['text'])
            if summary:
                final_post = f"⚡️ {summary}\n(Source: @{tweet['username']})"
                if len(final_post) > 280:
                    final_post = final_post[:277] + "..."
                post_tweet(final_post)
                save_posted_id(tweet_id)
        else:
            log.info(f"🟡 Ignored (not relevant): @{tweet['username']}: {tweet['text'][:80]}...")
