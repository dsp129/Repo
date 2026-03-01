from cryptography.fernet import Fernet
import os

def get_cipher():
    key = os.environ.get("ENCRYPTION_KEY")
    if not key:
        raise ValueError("ENCRYPTION_KEY not set in environment variables.")
    return Fernet(key.encode())

def encrypt_token(token: str) -> bytes:
    cipher = get_cipher()
    return cipher.encrypt(token.encode())

def decrypt_token(encrypted_token: bytes) -> str:
    cipher = get_cipher()
    return cipher.decrypt(encrypted_token).decode()