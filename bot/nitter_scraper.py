import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERNAMES_TXT = os.path.join(BASE_DIR, "usernames.txt")

def load_usernames_from_txt(filepath):
    usernames = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            username = line.strip().lstrip("@")
            if username:
                usernames.append(username)
    return usernames

def scrape_nitter(username, max_tweets=5, base_url="https://nitter.poast.org"):
    url = f"{base_url}/{username}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"⚠️ Failed to fetch {url}: Status {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        tweets = []

        for tweet in soup.select("div.timeline-item")[:max_tweets]:
            text_tag = tweet.select_one("div.tweet-content")
            date_tag = tweet.select_one("span.tweet-date > a")
            timestamp = date_tag["title"] if date_tag else None
            if text_tag and timestamp:
                tweets.append({
                    "username": username,
                    "text": text_tag.get_text(strip=True),
                    "timestamp": timestamp
                })

        return tweets

    except Exception as e:
        print(f"❌ Error scraping @{username}: {e}")
        return []

def scrape_all_nitter_users():
    usernames = load_usernames_from_txt(USERNAMES_TXT)
    print(f"📋 Loaded {len(usernames)} usernames")
    all_tweets = []

    for i, username in enumerate(usernames):
        print(f"🔎 Scraping @{username} via Nitter...")
        tweets = scrape_nitter(username)
        all_tweets.extend(tweets)
        time.sleep(1.5)  # throttle requests to avoid getting blocked

    return all_tweets

# Optional: test
if __name__ == "__main__":
    tweets = scrape_all_nitter_users()
    for tweet in tweets:
        print(f"[{tweet['timestamp']}] @{tweet['username']}: {tweet['text'][:100]}...")
