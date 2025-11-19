# Sync Daddy

This thing syncs songs at a best effort attempt from one music provider to another.  Right now, I only built the highway from Spotify to Apple Music.  With that being said, there are some spots that are built to extend the functionality to support multiple destination and source types, though there are other spots that are implemented in a very naive fashion.  Spare my feelings.

# Usage
Gotta have your whole environment setup, `cp .env.skel .env` and fill out the values accordingly.  Then you can just run `uv run python3 -m sync_daddy.main` and it'll go and do the things.

# Other things
I can set this up on a job to sync, dockerize and run an app somewhere to trigger a sync on demand, etc. But the one time is good enough for now.