from kiteconnect import KiteConnect
import os
import webbrowser

# ==============================
# READ API KEY & SECRET FROM FILES
# ==============================

def read_file(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename} not found.")
    with open(filename, "r") as f:
        return f.read().strip()

API_KEY = read_file("api_key.txt")
API_SECRET = read_file("api_secret.txt")

# ==============================
# GENERATE LOGIN URL
# ==============================

kite = KiteConnect(api_key=API_KEY)

print("\nOpening Zerodha login page...")
login_url = kite.login_url()
webbrowser.open(login_url)

print("\nAfter login, copy the 'request_token' from browser URL.")
request_token = input("Paste request_token here: ").strip()

# ==============================
# GENERATE ACCESS TOKEN
# ==============================

data = kite.generate_session(request_token, api_secret=API_SECRET)
access_token = data["access_token"]

print("\n✅ ACCESS TOKEN GENERATED SUCCESSFULLY\n")
print("Copy this access token and use it as environment variable:\n")
print(access_token)