# apps/api/signature/middleware.py
import re
import logging
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from .signer import verify_signature

logger = logging.getLogger(__name__)

class SignatureVerificationMiddleware(MiddlewareMixin):
    """
    Middleware untuk memverifikasi signature pada request ke /api/.
    Signature diharapkan ada di header 'X-Signature' dalam format base64.
    Body request digunakan sebagai payload untuk verifikasi.
    """

    def process_request(self, request):
        # Hanya terapkan pada endpoint API
       if not re.match(r'^/v1/api/', request.path):  # atau r'^/v\d+/api/' jika ingin fleksibel
        return None

        # Abaikan preflight CORS (OPTIONS)
        if request.method == 'OPTIONS':
            return None

        signature_b64 = request.headers.get('X-Signature')
        if not signature_b64:
            logger.warning("Missing X-Signature header for %s", request.path)
            return HttpResponseForbidden("Missing signature")

        # Decode signature dari base64
        import base64
        try:
            signature = base64.b64decode(signature_b64)
        except Exception:
            logger.warning("Invalid base64 in X-Signature")
            return HttpResponseForbidden("Invalid signature format")

        # Gunakan raw body (penting: jangan pakai request.POST atau request.data di sini)
        payload = request.body

        if not verify_signature(payload, signature):
            logger.warning("Signature verification failed for %s", request.path)
            return HttpResponseForbidden("Invalid signature")

        return None