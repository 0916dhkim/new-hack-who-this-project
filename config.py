# Module for discord bot configuration.

from dotenv import load_dotenv
import os


load_dotenv()
config = {
    "prefix": os.getenv("BOT_PREFIX"),
    "token": os.getenv("BOT_TOKEN"),
    "spotifyClientId": os.getenv("SPOTIFY_CLIENT_ID"),
    "spotifyClientSecret": os.getenv("SPOTIFY_CLIENT_SECRET"),
}
