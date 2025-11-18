from sync_daddy.services.factories import (
    get_apple_music_service,
    get_config_service,
    get_spotify_service,
)


def main() -> None:
    spotify = get_spotify_service()
    apple = get_apple_music_service()
    config_service = get_config_service()
    for replication in config_service.replications():
        # TODO: make a music provider factory function to return a music provider client
        # TODO: make a music provider client protocol for spotify and apple
        # TODO: make these smaller functions
        if replication.source.type == "spotify":
            source_tracks = spotify.get_all_tracks_for_playlist(
                replication.source.id, 100
            )
        else:
            raise Exception("I only support Spotify sources for now.")

        if replication.destination.type == "apple":
            destination_tracks = apple.get_playlist_tracks(replication.destination.id)
            destination_track_names_lower = [
                x.attributes.name.lower() for x in destination_tracks.data
            ]
            for song in source_tracks:
                songs_to_add = []
                if song.track.name.lower() not in destination_track_names_lower:
                    apple_song = apple.search_song(song.track.name)
                    if not apple_song.results:
                        print(
                            f"Could not find song: {song.track.name} in apple.  Add manually if necessary"
                        )
                        continue
                    songs_to_add.append(apple_song.results.songs.data[0].id)
                else:
                    print(f"Song exists in playlist {song.track.name}")
            if songs_to_add:
                apple.add_songs_to_playlist(songs_to_add, replication.destination.id)
        else:
            raise Exception("I only support Apple destinations for now.")


if __name__ == "__main__":
    main()
