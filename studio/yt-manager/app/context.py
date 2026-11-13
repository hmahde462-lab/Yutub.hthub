"""Wires settings, database, cipher and API factory together."""
from __future__ import annotations

from dataclasses import dataclass

from .config import Settings, get_settings
from .crypto import TokenCipher
from .db import Database
from .services import ServiceFactory
from .uploader import Uploader


@dataclass
class AppContext:
    settings: Settings
    db: Database
    cipher: TokenCipher
    services: ServiceFactory

    @property
    def uploader(self) -> Uploader:
        return Uploader(self.settings, self.db, self.cipher, self.services)


def build_context(settings: Settings | None = None) -> AppContext:
    settings = settings or get_settings()
    return AppContext(settings=settings, db=Database(settings.db_path),
                      cipher=TokenCipher(settings.encryption_key), services=ServiceFactory())
