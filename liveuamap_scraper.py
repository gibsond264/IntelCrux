import requests
from bs4 import BeautifulSoup

def scrape_liveuamap(region="ukraine"):
    url = f"https://{region}.liveuamap.com/"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        headlines = []
        for item in soup.select(".news_item"):
            text = item.get_text(strip=True)
            if any(kw in text.lower() for kw in ["missile", "strike", "rocket", "air raid", "explosion"]):
                headlines.append(text)

        return headlines
    except Exception as e:
        print("❌ Error scraping Liveuamap:", e)
        return []
