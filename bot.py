from kiteconnect import KiteConnect
import os
import time
from crypto_utils import decrypt_token

API_KEY = os.environ.get("API_KEY")

def load_token():
    if not os.path.exists("secure_token.bin"):
        raise FileNotFoundError("Token not generated yet.")
    with open("secure_token.bin", "rb") as f:
        encrypted = f.read()
    return decrypt_token(encrypted)

while True:
    try:
        access_token = load_token()

        kite = KiteConnect(api_key=API_KEY)
        kite.set_access_token(access_token)

        profile = kite.profile()
        print("Connected as:", profile["user_name"])

    except Exception as e:
        print("Waiting for login...", e)

    time.sleep(60)