import os
import tweepy
import csv
from dotenv import load_dotenv
from summarize import summarize_text
from logger import setup_logger

log = setup_logger()

load_dotenv()

auth = tweepy.OAuth1UserHandler(
    os.getenv("TWITTER_API_KEY"),
    os.getenv("TWITTER_API_SECRET"),
    os.getenv("TWITTER_ACCESS_TOKEN"),
    os.getenv("TWITTER_ACCESS_SECRET")
)
api = tweepy.API(auth)

# Get absolute paths based on current script location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTED_IDS_FILE = os.path.join(BASE_DIR, "posted_ids.txt")
FOLLOWERS_CSV = os.path.join(BASE_DIR, "followers.csv")

def load_posted_ids():
    if not os.path.exists(POSTED_IDS_FILE):
        return set()
    with open(POSTED_IDS_FILE, "r") as f:
        return set(line.strip() for line in f)

def save_posted_id(tweet_id):
    with open(POSTED_IDS_FILE, "a") as f:
        f.write(f"{tweet_id}\n")

def load_usernames_from_csv(filepath):
    usernames = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            username = row.get("username") or row.get("Username") or row.get("handle")
            if username:
                usernames.append(username.strip().lstrip("@"))
    return usernames

def is_relevant(text):
    keywords = [
        "missile", "airstrike", "strike", "IDF", "mobilization", "air raid",
        "explosion", "rocket", "drone", "nuclear", "counteroffensive", "invasion",
        "warplane", "ballistic", "intercept", "mobilized", "military", "border", "explosions"
    ]
    return any(kw.lower() in text.lower() for kw in keywords)

def post_tweet(text):
    try:
        api.update_status(status=text)
        log.info(f"✅ Posted: {text[:60]}...")
    except Exception as e:
        log.error(f"❌ Error posting: {e}")

def get_latest_tweets():
    usernames = load_usernames_from_csv(FOLLOWERS_CSV)
    posted_ids = load_posted_ids()

    for username in usernames:
        try:
            tweets = api.user_timeline(screen_name=username, count=5, tweet_mode="extended")
            for tweet in tweets:
                if str(tweet.id) in posted_ids:
                    continue
                if is_relevant(tweet.full_text):
                    log.info(f"[RELEVANT] @{username}: {tweet.full_text[:100]}...")
                    summary = summarize_text(tweet.full_text)
                    if summary:
                        final_post = f"⚡️ {summary}\n(Source: @{username})"
                        if len(final_post) > 280:
                            final_post = final_post[:277] + "..."
                        post_tweet(final_post)
                        save_posted_id(tweet.id)
        except Exception as e:
            log.error(f"❌ Error fetching @{username}: {e}")
