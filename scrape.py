from config import config
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import asyncio
from typing import Set, List
import csv


# Use spotipy package for maanaging access tokens.
if config["spotifyClientId"] is None:
    raise Exception("Environment variable SPOTIFY_CLIENT_ID is required.")
if config["spotifyClientSecret"] is None:
    raise Exception("Environment variable SPOTIFY_CLIENT_SECRET is required.")
spotifyCredentials = SpotifyClientCredentials(
    client_id=config["spotifyClientId"],
    client_secret=config["spotifyClientSecret"],
)
spotify = spotipy.Spotify(client_credentials_manager=spotifyCredentials)


class SpotifyTrack:
    def __init__(self, id, title, artist):
        self.id = id
        self.title = title
        self.artist = artist

    def __str__(self):
        return f"<[{self.id}] {self.title} ; {self.artist}>"


class SpotifyFeatures:
    def __init__(
        self,
        key,
        mode,
        acousticness,
        danceability,
        energy,
        instrumentalness,
        liveness,
        loudness,
        speechiness,
        valence,
        tempo,
    ):
        self.key = key
        self.mode = mode
        self.acousticness = acousticness
        self.danceability = danceability
        self.energy = energy
        self.instrumentalness = instrumentalness
        self.liveness = liveness
        self.loudness = loudness
        self.speechiness = speechiness
        self.valence = valence
        self.tempo = tempo


class Track:
    def __init__(
        self, spotifyTrack: SpotifyTrack, spotifyFeatures: SpotifyFeatures
    ):
        self.spotifyTrack = spotifyTrack
        self.spotifyFeatures = spotifyFeatures

    def __str__(self):
        return (
            f"<Track | {self.spotifyTrack.title} | "
            f"{self.spotifyTrack.artist}>"
        )

    def __eq__(self, other):
        return self.spotifyTrack.id == other.spotifyTrack.id

    def __hash__(self):
        return hash(self.spotifyTrack.id)


# All tracks.
allTracks: Set[Track] = set()


# Get categories.
async def getCategories():
    res = spotify.categories(country="US", limit=10)
    categoryIds = [i["id"] for i in res["categories"]["items"]]
    print(f"Scraping categories : {categoryIds}")
    await asyncio.gather(
        *[handleCategory(categoryId) for categoryId in categoryIds]
    )


# Get playlists from toplists category.
async def handleCategory(categoryId: str):
    res = spotify.category_playlists(categoryId, country="US", limit=10)
    playlistIds = [i["id"] for i in res["playlists"]["items"]]
    await asyncio.gather(
        *[handlePlaylist(playlist) for playlist in playlistIds]
    )


# Get tracks in playlist.
async def handlePlaylist(playlistId: str):
    res = spotify.playlist_tracks(playlistId)
    spotifyTrackData = [i["track"] for i in res["items"]]
    spotifyTracks: List[SpotifyTrack] = []
    for track in spotifyTrackData:
        try:
            spotifyTracks.append(
                SpotifyTrack(
                    track["id"], track["name"], track["artists"][0]["name"]
                )
            )
        except Exception as e:
            print(f"Failed to add a track from playlist {playlistId}")
            print(e)
            continue
    await asyncio.gather(
        *[handleSpotifyTrack(track) for track in spotifyTracks]
    )


async def handleSpotifyTrack(spotifyTrack: SpotifyTrack):
    features = await getSpotifyFeatures(spotifyTrack.id)
    if features is None:
        return
    track = Track(spotifyTrack, features)
    print(track)
    allTracks.add(track)


async def getSpotifyFeatures(trackId: str):
    [res] = spotify.audio_features([trackId])
    if res is None:
        return None
    return SpotifyFeatures(
        res["key"],
        res["mode"],
        res["acousticness"],
        res["danceability"],
        res["energy"],
        res["instrumentalness"],
        res["liveness"],
        res["loudness"],
        res["speechiness"],
        res["valence"],
        res["tempo"],
    )


if __name__ == "__main__":
    asyncio.run(getCategories())
    with open("scraped.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "spotify_id",
            "title",
            "artist",
            "key",
            "mode",
            "acousticness",
            "danceability",
            "energy",
            "instrumentalness",
            "liveness",
            "loudness",
            "speechiness",
            "valence",
            "tempo",
        ]
        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames,
            quoting=csv.QUOTE_NONNUMERIC,
            lineterminator="\n",
        )
        writer.writeheader()
        for track in allTracks:
            writer.writerow(
                {
                    "spotify_id": track.spotifyTrack.id,
                    "title": track.spotifyTrack.title,
                    "artist": track.spotifyTrack.artist,
                    "key": track.spotifyFeatures.key,
                    "mode": track.spotifyFeatures.mode,
                    "acousticness": track.spotifyFeatures.acousticness,
                    "danceability": track.spotifyFeatures.danceability,
                    "energy": track.spotifyFeatures.energy,
                    "instrumentalness": track.spotifyFeatures.instrumentalness,
                    "liveness": track.spotifyFeatures.liveness,
                    "loudness": track.spotifyFeatures.loudness,
                    "speechiness": track.spotifyFeatures.speechiness,
                    "valence": track.spotifyFeatures.valence,
                    "tempo": track.spotifyFeatures.tempo,
                }
            )
