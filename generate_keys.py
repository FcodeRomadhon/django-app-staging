# generate_keys.py
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import base64

private_key = Ed25519PrivateKey.generate()
public_key = private_key.public_key()

# Gunakan metode *_raw() — ini adalah cara resmi di versi baru
private_bytes = private_key.private_bytes_raw()   # returns 32-byte bytes
public_bytes = public_key.public_bytes_raw()      # returns 32-byte bytes

print("PRIVATE_KEY_BASE64 =", base64.b64encode(private_bytes).decode())
print("PUBLIC_KEY_BASE64  =", base64.b64encode(public_bytes).decode())