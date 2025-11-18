import httpx
from pydantic import BaseModel


class Track(BaseModel):
    name: str


class PlaylistTrack(BaseModel):
    track: Track


class PlaylistTracksResponse(BaseModel):
    next: str | None
    items: list[PlaylistTrack]


class TokenRequestResponse(BaseModel):
    access_token: str


class SpotifyService:
    def __init__(self, client_id: str, client_secret: str) -> None:
        token = self._request_access_token(client_id, client_secret)
        self._client = httpx.Client(
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def get_playlist_tracks(
        self, playlist_id: str, limit: int = 100, offset: int = 0
    ) -> PlaylistTracksResponse:
        response = self._client.get(
            f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
            params={"offset": offset, "limit": limit},
        )
        response.raise_for_status()
        return PlaylistTracksResponse.model_validate(response.json())

    def get_all_tracks_for_playlist(
        self, playlist_id: str, limit: int
    ) -> list[PlaylistTrack]:
        tracks: list[PlaylistTrack] = []
        offset = 0
        while True:
            response = self.get_playlist_tracks(playlist_id, limit=limit, offset=offset)
            tracks.extend(response.items)
            if response.next is not None:
                offset += limit
            else:
                break
        return tracks

    def _request_access_token(self, client_id: str, client_secret: str) -> str:
        response = httpx.post(
            "https://accounts.spotify.com/api/token",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "accept": "application/json",
            },
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
            },
        )
        response.raise_for_status()
        return TokenRequestResponse.model_validate(response.json()).access_token
