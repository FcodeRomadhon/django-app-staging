# apps/api/signature/keys.py
import os
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

load_dotenv()

def get_private_key() -> Ed25519PrivateKey:
    """Muat private key dari environment variable PRIVATE_KEY_BASE64."""
    private_key_b64 = os.getenv("PRIVATE_KEY_BASE64")
    if not private_key_b64:
        raise EnvironmentError("Environment variable PRIVATE_KEY_BASE64 is not set.")
    
    # Decode dari base64
    import base64
    private_bytes = base64.b64decode(private_key_b64)
    return Ed25519PrivateKey.from_private_bytes(private_bytes)

def get_public_key() -> Ed25519PublicKey:
    """Muat public key dari environment variable PUBLIC_KEY_BASE64."""
    public_key_b64 = os.getenv("PUBLIC_KEY_BASE64")
    if not public_key_b64:
        raise EnvironmentError("Environment variable PUBLIC_KEY_BASE64 is not set.")
    
    import base64
    public_bytes = base64.b64decode(public_key_b64)
    return Ed25519PublicKey.from_public_bytes(public_bytes)