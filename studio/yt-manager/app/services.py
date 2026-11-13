"""Builds Google API clients. Kept separate so tests can inject fakes."""
from __future__ import annotations

from googleapiclient.discovery import build


class ServiceFactory:
    def youtube(self, credentials):
        return build("youtube", "v3", credentials=credentials, cache_discovery=False)

    def analytics(self, credentials):
        return build("youtubeAnalytics", "v2", credentials=credentials, cache_discovery=False)
