# IntelCrux OSINT Bot & Dashboard

IntelCrux is an automated OSINT system that monitors trusted Twitter/X accounts and geopolitical news sources, summarizes key events using AI, and posts real-time updates. It also includes a simple web dashboard to view logs.

---

## 🚀 Features

- 🛰️ Monitors OSINT & conflict-focused X accounts
- 🧠 Uses OpenAI to summarize tweets and Liveuamap events
- 📤 Posts real-time updates via your @IntelCrux X account
- 🗂 Logs all actions to a file (`bot.log`)
- 🌐 Live dashboard (Flask) to view log activity

---

## 📁 Project Structure

```
intelcrux/
├── bot/
│   ├── main.py              # scheduled OSINT runner
│   ├── twitter_monitor.py   # filters tweets & posts
│   ├── summarize.py         # GPT-3.5 summarization
│   ├── liveuamap_scraper.py # optional Liveuamap scraping
│   ├── logger.py            # shared logging logic
│   ├── posted_ids.txt       # used to prevent duplicate tweets
│   ├── requirements.txt
│   └── .env.example
│
├── dashboard/
│   ├── dashboard.py         # Flask dashboard to show logs
│   ├── logger.py
│   └── requirements.txt
│
├── .github/
│   └── workflows/
│       └── deploy.yml       # GitHub Actions for Railway auto-deploy
│
├── .gitignore
└── README.md
```

---

## 🧑‍💻 Setup Instructions

### 🔧 1. Local Environment

```bash
cd bot
cp .env.example .env  # fill in your keys
pip install -r requirements.txt
python main.py
```

In a second terminal:

```bash
cd dashboard
pip install -r requirements.txt
python dashboard.py
```

Dashboard will be live at [http://localhost:8080](http://localhost:8080)

---

## ☁️ Deployment with Railway

- Push this repo to GitHub
- Deploy each folder as a separate **Railway service**:
  - bot/: `python main.py`
  - dashboard/: `python dashboard.py`
- Add your `.env` values under Railway → Project → Variables

---

## 🔄 Auto Deploy via GitHub Actions

Set a GitHub secret:
- **RAILWAY_TOKEN** (from https://railway.app/account/tokens)

Workflow triggers on push to `main` and deploys both services automatically.

---

## ✅ API Keys Needed

| Key                     | Use                       |
|------------------------|---------------------------|
| TWITTER_API_KEY         | Twitter/X developer app   |
| TWITTER_API_SECRET      |                           |
| TWITTER_BEARER_TOKEN    |                           |
| TWITTER_ACCESS_TOKEN    |                           |
| TWITTER_ACCESS_SECRET   |                           |
| OPENAI_API_KEY          | GPT-3.5 for summarization |

---

## 🛡 Notes

- 🔐 Never commit `.env` or `bot.log`
- 📈 You can enhance dashboard with filters, search, auth
- 💬 DM alerts, Telegram, and database logging coming soon

---

Built with ❤️ by IntelCrux.
