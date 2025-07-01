# IntelCrux OSINT Bot

An OSINT news‐bot that automatically fetches and summarizes live geopolitical updates from LiveUAMap and selected Telegram channels, then posts them (with optional media) into your Telegram chat.

---

## Features

- **LiveUAMap RSS**: Pulls and summarizes the latest headlines for `ukraine` and `israel`.
- **Telegram Channels**: Scrapes the last 30 minutes of messages (and any attached media) from your configured Telegram channels.
- **AI Summaries**: Uses a HuggingFace/BART summarizer with dynamic length settings for clean, concise, English‐language summaries.
- **Deduplication**: Avoids reposting the same story (by message‐ID and summary hash).
- **Telegram Delivery**: Posts either text or photo+caption to your specified Telegram chat via the Bot API.
- **Configurable Schedule**: Runs both jobs every 5 minutes by default (adjustable in `main.py`).

---

## 📋 Requirements

- Python 3.11+
- Pip  
- A Telegram **Bot Token** (from [@BotFather](https://t.me/BotFather))
- Your **Chat ID** (group or channel) for bot delivery  
- Telegram **API ID** & **API Hash** (from https://my.telegram.org)

---

## 🚀 Installation

1. **Clone** this repository:
   ```bash
   git clone https://github.com/your-user/intelcrux.git
   cd intelcrux

