from pydantic import BaseModel
from dotenv import load_dotenv
import os
import yaml
from typing import Tuple


load_dotenv()


class PlaylistProvider(BaseModel):
    id: str
    type: str


class Replication(BaseModel):
    source: PlaylistProvider
    destination: PlaylistProvider


class SpotifyConfig(BaseModel):
    client_id_key: str
    client_secret_key: str


class AppleConfig(BaseModel):
    key_id_key: str
    team_id_key: str
    private_key_contents_key: str
    music_user_token_key: str


class Config(BaseModel):
    spotify: SpotifyConfig
    apple: AppleConfig
    replications: list[Replication]


class ConfigService:
    def __init__(self) -> None:
        try:
            with open(f"sync_daddy/config/{os.environ['ENV']}.yaml", "r") as f:
                self._config = Config.model_validate(yaml.safe_load(f))
        except Exception as e:
            print(f"Failed to parse config {e}")
            raise e

    def spotify_config(self) -> Tuple[str, str]:
        return (
            os.environ[self._config.spotify.client_id_key],
            os.environ[self._config.spotify.client_secret_key],
        )

    def replications(self) -> list[Replication]:
        return self._config.replications

    def apple_config(self) -> Tuple[str, str, str, str]:
        return (
            os.environ[self._config.apple.team_id_key],
            os.environ[self._config.apple.key_id_key],
            os.environ[self._config.apple.private_key_contents_key],
            os.environ[self._config.apple.music_user_token_key],
        )
