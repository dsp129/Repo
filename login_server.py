from flask import Flask, request
from kiteconnect import KiteConnect
import os
from crypto_utils import encrypt_token

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")

kite = KiteConnect(api_key=API_KEY)

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

try:
    send_telegram("✅ Zerodha Login Successful 🚀")
except Exception as e:
    print("Telegram Error:", e)

return "✅ Login successful. Token securely stored."
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
