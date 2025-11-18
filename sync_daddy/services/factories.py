from sync_daddy.services.apple import AppleMusicService
from sync_daddy.services.config_service import ConfigService
from sync_daddy.services.spotify import SpotifyService


def get_config_service() -> ConfigService:
    return ConfigService()


def get_spotify_service() -> SpotifyService:
    config_service = get_config_service()
    client_id, client_secret = config_service.spotify_config()
    return SpotifyService(client_id, client_secret)


def get_apple_music_service() -> AppleMusicService:
    config_service = get_config_service()
    team_id, key_id, private_key, music_user_token = config_service.apple_config()
    return AppleMusicService(key_id, team_id, private_key, music_user_token)
