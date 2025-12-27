from dataclasses import dataclass
from typing import Any

from spotipy.oauth2 import SpotifyOAuth

from spotify_rag.utils import Settings


@dataclass
class SpotifyAuthManager:
    _oauth: SpotifyOAuth | None = None

    @property
    def oauth(self) -> SpotifyOAuth:
        """Get or create the SpotifyOAuth instance."""
        if self._oauth is None:
            self._oauth = SpotifyOAuth(
                client_id=Settings.SPOTIFY_CLIENT_ID,
                client_secret=Settings.SPOTIFY_CLIENT_SECRET,
                redirect_uri=Settings.SPOTIFY_REDIRECT_URI,
                scope=Settings.SPOTIFY_SCOPES,
                cache_path=str(Settings.CACHE_PATH / ".spotify_cache"),
                show_dialog=True,
            )
        return self._oauth

    def get_auth_url(self) -> str:
        return self.oauth.get_authorize_url()

    def get_access_token(self, code: str) -> dict[str, Any] | None:
        try:
            return self.oauth.get_access_token(code, as_dict=True)
        except Exception:
            return None

    def get_cached_token(self) -> dict[str, Any] | None:
        return self.oauth.get_cached_token()

    def refresh_token(self, refresh_token: str) -> dict[str, Any] | None:
        try:
            return self.oauth.refresh_access_token(refresh_token)
        except Exception:
            return None
