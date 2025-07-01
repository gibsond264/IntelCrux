import os
import time
import requests
from bs4 import BeautifulSoup

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

def scrape_nitter(username, max_tweets=5):
    mirrors = [
        "https://nitter.privacydev.net",
        "https://nitter.lacontrevoie.fr",
        "https://nitter.poast.org",
        "https://nitter.net"
    ]
    headers = {"User-Agent": "Mozilla/5.0"}

    for base_url in mirrors:
        url = f"{base_url}/{username}"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"⚠️ Mirror {base_url} failed for @{username}: Status {response.status_code}")
                continue

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

            print(f"✅ Scraped @{username} from {base_url}")
            return tweets

        except Exception as e:
            print(f"❌ Error scraping @{username} via {base_url}: {e}")
            time.sleep(1)  # pause before trying next mirror

    print(f"❌ All Nitter mirrors failed for @{username}")
    return []

def scrape_all_nitter_users():
    usernames = load_usernames_from_txt(USERNAMES_TXT)
    print(f"📋 Loaded {len(usernames)} usernames")
    all_tweets = []

    for i, username in enumerate(usernames):
        print(f"🔎 Scraping @{username} via Nitter...")
        tweets = scrape_nitter(username)
        all_tweets.extend(tweets)
        time.sleep(1.5)  # throttle between users

    return all_tweets

# Optional: test run
if __name__ == "__main__":
    tweets = scrape_all_nitter_users()
    for tweet in tweets:
        print(f"[{tweet['timestamp']}] @{tweet['username']}: {tweet['text'][:100]}...")
