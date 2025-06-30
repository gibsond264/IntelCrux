# summarize.py
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_text(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an OSINT analyst writing concise, neutral summaries of geopolitical alerts."},
                {"role": "user", "content": f"Summarize this tweet clearly in 1-2 sentences for a real-time conflict update:\n\n{text}"}
            ],
            max_tokens=100,
            temperature=0.6
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ OpenAI error:", e)
        return None
