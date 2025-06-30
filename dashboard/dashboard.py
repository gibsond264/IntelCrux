from flask import Flask, render_template_string
import os

app = Flask(__name__)

@app.route("/")
def home():
    log_path = "bot.log"
    if not os.path.exists(log_path):
        return "No log file yet. Bot may not have written logs."

    try:
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()[-50:]
    except Exception as e:
        return f"Error reading log: {e}"

    html_template = """
    <html>
        <head><title>IntelCrux Logs</title></head>
        <body style='font-family: monospace; background: #111; color: #0f0; padding: 20px;'>
            <h2>IntelCrux Log Dashboard</h2>
            <pre>{{ log_content }}</pre>
        </body>
    </html>
    """

    return render_template_string(html_template, log_content="".join(lines))
from flask import Flask, render_template_string
import os

app = Flask(__name__)

@app.route("/")
def home():
    log_path = "bot.log"

    if not os.path.exists(log_path):
        # Create a temporary dummy log file to avoid crashes
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("✅ Log initialized. Waiting for bot activity...\n")

    try:
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()[-50:]
    except Exception as e:
        return f"Error reading log file: {e}"

    html_template = """
    <html>
        <head><title>IntelCrux Logs</title></head>
        <body style='font-family: monospace; background: #111; color: #0f0; padding: 20px;'>
            <h2>IntelCrux Log Dashboard</h2>
            <pre>{{ log_content }}</pre>
        </body>
    </html>
    """

    return render_template_string(html_template, log_content="".join(lines))
