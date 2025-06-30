import os
import time
import tweepy
from dotenv import load_dotenv
from summarize import summarize_text
from logger import setup_logger
from datetime import datetime, timezone, timedelta
from liveuamap_scraper import scrape_liveuamap

log = setup_logger()

load_dotenv()

# v1.1 API (for posting)
auth = tweepy.OAuth1UserHandler(
    os.getenv("TWITTER_API_KEY"),
    os.getenv("TWITTER_API_SECRET"),
    os.getenv("TWITTER_ACCESS_TOKEN"),
    os.getenv("TWITTER_ACCESS_SECRET")
)
api = tweepy.API(auth)

# v2 API (for reading/searching)
client = tweepy.Client(bearer_token=os.getenv("TWITTER_BEARER_TOKEN"))

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTED_IDS_FILE = os.path.join(BASE_DIR, "posted_ids.txt")
USERNAMES_TXT = os.path.join(BASE_DIR, "usernames.txt")

def load_posted_ids():
    if not os.path.exists(POSTED_IDS_FILE):
        return set()
    with open(POSTED_IDS_FILE, "r") as f:
        return set(line.strip() for line in f)

def save_posted_id(tweet_id):
    with open(POSTED_IDS_FILE, "a") as f:
        f.write(f"{tweet_id}\n")

def load_usernames_from_txt(filepath):
    usernames = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            username = line.strip().lstrip("@")
            if username:
                usernames.append(username)
    return usernames

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
    usernames = load_usernames_from_txt(USERNAMES_TXT)
    log.info(f"📋 Loaded usernames: {usernames}")
    posted_ids = load_posted_ids()
    time_threshold = datetime.now(timezone.utc) - timedelta(minutes=15)

    for i, username in enumerate(usernames):
        if i >= 40:
            log.info("⚠️ Limit reached: skipping remaining usernames to stay under Twitter API rate limits.")
            break

        try:
            query = f"from:{username} -is:retweet"
            tweets = client.search_recent_tweets(
                query=query,
                tweet_fields=["created_at", "text", "id"],
                max_results=5
            )

            results = tweets.data or []
            log.info(f"📥 Fetched {len(results)} tweets from @{username}")

            for tweet in results:
                if tweet.created_at < time_threshold:
                    log.info(f"⏰ Skipped old tweet from @{username} (created at {tweet.created_at})")
                    continue

                if str(tweet.id) in posted_ids:
                    log.info(f"⏩ Skipped duplicate tweet ID {tweet.id} from @{username}")
                    continue

                if is_relevant(tweet.text):
                    log.info(f"[RELEVANT] @{username}: {tweet.text[:100]}...")
                    summary = summarize_text(tweet.text)
                    if summary:
                        final_post = f"⚡️ {summary}\n(Source: @{username})"
                        if len(final_post) > 280:
                            final_post = final_post[:277] + "..."
                        post_tweet(final_post)
                        save_posted_id(tweet.id)
                else:
                    log.info(f"🟡 Ignored (not relevant): @{username}: {tweet.text[:80]}...")

            time.sleep(1.5)

        except Exception as e:
            log.error(f"❌ Error fetching @{username} via v2 API: {e}")
            time.sleep(2)

def check_liveuamap_scraper():
    log.info("🔎 Checking Liveuamap scraper...")
    for region in ["ukraine", "israel"]:
        headlines = scrape_liveuamap(region)
        if not headlines:
            log.warning(f"⚠️ No headlines scraped from Liveuamap for region: {region}")
        else:
            log.info(f"✅ {len(headlines)} headlines scraped from Liveuamap for {region}")

