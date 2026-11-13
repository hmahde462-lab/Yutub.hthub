"""Encryption of OAuth credentials at rest (Fernet = AES-128-CBC + HMAC-SHA256)."""
from __future__ import annotations

from cryptography.fernet import Fernet, InvalidToken


class CryptoError(RuntimeError):
    pass


def generate_key() -> str:
    return Fernet.generate_key().decode()


class TokenCipher:
    def __init__(self, key: str | None):
        if not key:
            raise CryptoError(
                "YTM_ENCRYPTION_KEY غير موجود. أنشئ مفتاحاً بالأمر: python -m app.cli init-key"
            )
        try:
            self._fernet = Fernet(key.encode())
        except (ValueError, TypeError) as exc:
            raise CryptoError("YTM_ENCRYPTION_KEY غير صالح") from exc

    def encrypt(self, plaintext: str) -> bytes:
        return self._fernet.encrypt(plaintext.encode("utf-8"))

    def decrypt(self, token: bytes) -> str:
        try:
            return self._fernet.decrypt(token).decode("utf-8")
        except InvalidToken as exc:
            raise CryptoError("تعذر فك تشفير بيانات القناة (المفتاح تغيّر؟)") from exc
