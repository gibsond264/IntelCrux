from flask import Flask, render_template_string
import os

app = Flask(__name__)

@app.route("/")
def home():
    log_path = "bot.log"

    if not os.path.exists(log_path):
        return "No logs found. The bot may not have written anything yet."

    with open(log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()[-50:]

    html_template = '''
    <html>
        <head><title>IntelCrux Logs</title></head>
        <body style='font-family: monospace; background: #111; color: #0f0; padding: 20px;'>
            <h2>IntelCrux Log Dashboard</h2>
            <pre>{{ log_content }}</pre>
        </body>
    </html>
    '''

    return render_template_string(html_template, log_content="".join(lines))
