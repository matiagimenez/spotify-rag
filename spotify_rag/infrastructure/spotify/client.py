"""Spotify API client wrapper using spotipy."""

from typing import Any

from pydantic import BaseModel
from spotipy import Spotify

from spotify_rag.domain import SpotifyUser


class SpotifyClient(BaseModel):
    access_token: str

    @property
    def client(self) -> Spotify:
        return Spotify(auth=self.access_token)

    @property
    def current_user(self) -> SpotifyUser:
        user_data = self.client.current_user()
        return SpotifyUser.from_api_response(user_data)

    def get_liked_songs(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        return self.client.current_user_saved_tracks(limit=limit, offset=offset)

    def get_all_liked_songs(self, max_tracks: int = 500) -> list[dict[str, Any]]:
        """Fetch all liked songs with pagination.

        Args:
            max_tracks: Maximum number of tracks to fetch.

        Returns:
            List of all saved track items.
        """
        all_tracks: list[dict[str, Any]] = []
        offset = 0
        limit = 50

        while offset < max_tracks:
            response = self.get_liked_songs(limit=limit, offset=offset)
            items = response.get("items", [])

            if not items:
                break

            all_tracks.extend(items)
            offset += limit

            if len(items) < limit:
                break

        return all_tracks[:max_tracks]

    def get_audio_features(
        self,
        track_ids: list[str],
    ) -> list[dict[str, Any] | None]:
        """Get audio features for multiple tracks.

        Args:
            track_ids: List of Spotify track IDs (max 100 per call).

        Returns:
            List of audio features for each track.
        """
        # Spotify API limits to 100 tracks per request
        batch_size = 100
        all_features: list[dict[str, Any] | None] = []

        for i in range(0, len(track_ids), batch_size):
            batch = track_ids[i : i + batch_size]
            features = self._client.audio_features(batch)
            all_features.extend(features)

        return all_features
