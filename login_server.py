from flask import Flask, request
from kiteconnect import KiteConnect
import os
import requests
from crypto_utils import encrypt_token

app = Flask(__name__)

# ===== ENV VARIABLES =====
API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

kite = KiteConnect(api_key=API_KEY)

# ===== TELEGRAM FUNCTION =====
def send_telegram(msg):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": msg
        })

# ===== ROUTES =====
@app.route("/")
def home():
    return f'<a href="{kite.login_url()}">Login with Zerodha</a>'

@app.route("/callback")
def callback():
    request_token = request.args.get("request_token")

    data = kite.generate_session(request_token, api_secret=API_SECRET)
    access_token = data["access_token"]

    encrypted = encrypt_token(access_token)

    with open("secure_token.bin", "wb") as f:
        f.write(encrypted)

    send_telegram("✅ Zerodha Login Successful 🚀")

    return "✅ Login successful. Token securely stored."

# 🔥 DAILY REPORT ROUTE (OUTSIDE callback)
@app.route("/daily-report")
def daily_report():
    pnl = "₹ 0 (Test Mode)"
    send_telegram(f"📊 Daily Report\nPnL: {pnl}")
    return "Report Sent"

@app.route("/health")
def health():
    send_telegram("🟢 AlgoBot Running OK")
    return "OK"

@app.route("/test")
def test():
    send_telegram("Flask Route Test 🚀")
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
