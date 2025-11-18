import jwt
import time

import httpx
from pydantic import BaseModel, Field


class SongAttributes(BaseModel):
    artistName: str
    name: str


class Song(BaseModel):
    id: str
    attributes: SongAttributes


class LibrarySongs(BaseModel):
    data: list[Song]


class LibrarySearchResults(BaseModel):
    library_songs: LibrarySongs | None = Field(default=None, alias="library-songs")


class LibrarySearchResponse(BaseModel):
    results: LibrarySearchResults


class PlaylistTrackResponse(BaseModel):
    next: str | None = None
    data: list[Song]


class CatalogSearchSongResults(BaseModel):
    data: list[Song]


class CatalogSearchResults(BaseModel):
    songs: CatalogSearchSongResults


class CatalogSearchResponse(BaseModel):
    results: CatalogSearchResults


class AppleMusicService:
    def __init__(
        self,
        key_id: str,
        team_id: str,
        key_contents: str,
        music_user_token: str,
        signing_algorithm: str = "ES256",
    ) -> None:
        token = self._get_token(key_id, team_id, key_contents)
        self._client = httpx.Client(
            headers={
                "Authorization": f"Bearer {token}",
                "Music-User-Token": music_user_token,
            }
        )

    # TODO: write a paginator over this.  The initial playlist i'm going to sync has
    #       74 songs, and I don't have an apple playlist example handy that i'd need pagination for
    def get_playlist_tracks(
        self, playlist_id: str, limit: int = 100
    ) -> PlaylistTrackResponse:
        response = self._client.get(
            f"https://api.music.apple.com/v1/me/library/playlists/{playlist_id}/tracks",
            params={"limit": limit},
        )
        response.raise_for_status()
        return PlaylistTrackResponse.model_validate(response.json())

    def add_songs_to_playlist(self, song_ids: list[str], playlist_id: str) -> None:
        response = self._client.post(
            f"https://api.music.apple.com/v1/me/library/playlists/{playlist_id}/tracks",
            json={
                "data": [
                    {"id": song_id, "type": "library-songs"} for song_id in song_ids
                ]
            },
        )
        response.raise_for_status()

    def search_song(self, song_title: str, limit: int = 1) -> CatalogSearchResponse:
        response = self._client.get(
            "https://api.music.apple.com/v1/catalog/us/search",
            params={
                "term": song_title,
                "types": ["songs"],
                "limit": limit,
            },
        )
        response.raise_for_status()
        return CatalogSearchResponse.model_validate(response.json())

    def _get_token(
        self,
        key_id: str,
        team_id: str,
        key_contents: str,
        signing_algorithm: str = "ES256",
    ) -> str:
        headers = {"kid": key_id, "alg": signing_algorithm}

        now = int(time.time())

        SIX_MONTHS_IN_SECONDS = 15777000

        payload = {"iss": team_id, "iat": now, "exp": now + SIX_MONTHS_IN_SECONDS}
        token = jwt.encode(
            payload, key_contents, algorithm=signing_algorithm, headers=headers
        )
        return token
