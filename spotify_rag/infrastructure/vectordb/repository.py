"""ChromaDB vector database repository."""

from typing import Optional

from chromadb import Collection, PersistentClient
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from pydantic import BaseModel

from spotify_rag.domain import EnrichedTrack
from spotify_rag.utils import LogLevel, Settings, log


class VectorDBRepository(BaseModel):
    """Repository for ChromaDB vector database operations."""

    _client: Optional[PersistentClient] = None

    @property
    def client(self) -> PersistentClient:
        """Lazy-load persistent ChromaDB client."""
        if self._client is None:
            Settings.CHROMADB_PATH.mkdir(parents=True, exist_ok=True)
            log(
                f"Initializing Chr  omaDB client at {Settings.CHROMADB_PATH}",
                LogLevel.INFO,
            )
            self._client = PersistentClient(path=str(Settings.CHROMADB_PATH))
        return self._client

    @property
    def collection(self) -> Collection:
        return self.get_or_create_collection()

    def get_or_create_collection(self) -> Collection:
        """Get or create a collection by name with cosine similarity."""
        return self.client.get_or_create_collection(
            name=Settings.CHROMADB_COLLECTION,
            embedding_function=OllamaEmbeddingFunction(
                model_name=Settings.EMBEDDING_MODEL
            ),
            metadata={"hnsw:space": "cosine"},  # Use cosine similarity
        )

    def add_track(self, enriched_track: EnrichedTrack) -> None:
        """Add a single enriched track to the collection."""
        if not enriched_track.vibe_description:
            return

        track = enriched_track.track.track
        metadata = {
            "track_id": enriched_track.track_id,
            "track_name": track.name,
            "artist_names": track.artist_names,
            "album_name": track.album.name,
            "has_lyrics": enriched_track.has_lyrics,
            "genres": ", ".join(artist.genre_names for artist in track.artists),
            "popularity": track.popularity,
            "spotify_url": track.spotify_url or "",
        }

        self.collection.add(
            ids=[enriched_track.track_id],
            documents=[enriched_track.vibe_description],
            metadatas=[metadata],
        )

    def add_tracks(self, enriched_tracks: list[EnrichedTrack]) -> None:
        """Add multiple enriched tracks to the collection."""
        log(f"Adding {len(enriched_tracks)} tracks to VectorDB...", LogLevel.INFO)
        for enriched_track in enriched_tracks:
            self.add_track(enriched_track)
        log("Successfully added tracks to VectorDB.", LogLevel.INFO)

    def delete_tracks(self, track_ids: list[str]) -> None:
        log(f"Deleting {len(track_ids)} tracks from VectorDB...", LogLevel.INFO)
        self.collection.delete(ids=track_ids)
