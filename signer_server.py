# signer_server.py
from flask import Flask, request, jsonify
import base64
import os
import logging
from dotenv import load_dotenv
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('signature')

load_dotenv()
app = Flask(__name__)

@app.route('/sign', methods=['POST'])
def sign():
    body = request.get_data()
    body_str = body.decode('utf-8', errors='replace')
    logger.info(f"📩 Received sign request")
    logger.info(f"Body to sign: {body_str}")

    try:
        private_key_b64 = os.getenv("PRIVATE_KEY_BASE64")
        if not private_key_b64:
            raise EnvironmentError("PRIVATE_KEY_BASE64 not set")

        private_key = Ed25519PrivateKey.from_private_bytes(
            base64.b64decode(private_key_b64)
        )
        signature = private_key.sign(body)
        sig_b64 = base64.b64encode(signature).decode()

        logger.info(f"✅ Signature generated: {sig_b64[:32]}...")  # log 32 char pertama
        return jsonify({"signature": sig_b64})

    except Exception as e:
        logger.error(f"❌ Sign error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logger.info("🚀 Signer server running on http://localhost:5001/sign")
    app.run(host='127.0.0.1', port=5001, debug=False)