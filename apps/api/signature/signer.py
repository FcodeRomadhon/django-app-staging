# apps/api/signature/signer.py
from .keys import get_private_key, get_public_key

def sign_data(data: bytes) -> bytes:
    """
    Tandatangani data menggunakan private key Ed25519.
    Mengembalikan signature dalam bentuk bytes (64 byte).
    """
    private_key = get_private_key()
    return private_key.sign(data)

def verify_signature(data: bytes, signature: bytes) -> bool:
    """
    Verifikasi apakah signature valid untuk data tertentu.
    Mengembalikan True jika valid, False jika tidak.
    """
    public_key = get_public_key()
    try:
        public_key.verify(signature, data)
        return True
    except Exception:
        return False