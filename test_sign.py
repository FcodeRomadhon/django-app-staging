# test_sign.py
import base64
import os
from dotenv import load_dotenv  # ← tambahkan ini
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

# Muat file .env dari folder saat ini
load_dotenv()

private_key_b64 = os.getenv("PRIVATE_KEY_BASE64")
if not private_key_b64:
    raise EnvironmentError("PRIVATE_KEY_BASE64 not found in .env")

private_bytes = base64.b64decode(private_key_b64)
private_key = Ed25519PrivateKey.from_private_bytes(private_bytes)

body = b'{"id_user": 47, "app_versi": "VERVAL,2.1.0"}'
signature = private_key.sign(body)
sig_b64 = base64.b64encode(signature).decode()

print("Body:", body.decode())
print("X-Signature:", sig_b64)