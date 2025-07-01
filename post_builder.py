import random

def build_post(summary, source=None, tag=None):
    templates = [
        "⚡️ {summary}\n🔍 Source: {source}",
        "🧠 Summary:\n{summary}\n🛰️ {source}",
        "🌍 {summary}\n➡️ Update via {source}",
        "📢 {summary}\n#IntelCrux {tag}"
    ]
    template = random.choice(templates)
    return template.format(summary=summary, source=source or "Liveuamap", tag=tag or "OSINT")
