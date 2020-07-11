from config import config
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pylast
import asyncio
import httpx
from typing import List
import os


# Use spotipy package for maanaging access tokens.
if config["spotifyClientId"] is None:
    raise Exception("Environment variable SPOTIFY_CLIENT_ID is required.")
if config["spotifyClientSecret"] is None:
    raise Exception("Environment variable SPOTIFY_CLIENT_SECRET is required.")
if config["lastFmKey"] is None:
    raise Exception("Environment varialbe LASTFM_API_KEY is required.")
if config["lastFmSecret"] is None:
    raise Exception("Environment varialbe LASTFM_API_SECRET is required.")
spotifyCredentials = SpotifyClientCredentials(
    client_id=config["spotifyClientId"], client_secret=config["spotifyClientSecret"]
)
spotify = spotipy.Spotify(client_credentials_manager=spotifyCredentials)
lastfm = pylast.LastFMNetwork(
    api_key=config["lastFmKey"], api_secret=config["lastFmSecret"]
)


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
    def __init__(self, spotifyTrack, spotifyFeatures, tags):
        self.spotifyTrack = spotifyTrack
        self.spotifyFeatures = spotifyFeatures
        self.tags = tags

    def __str__(self):
        return f"<Track | {self.spotifyTrack.title} | {self.spotifyTrack.artist} | {self.tags}>"


# All tracks.
allTracks: List[Track] = []


# Get playlists from toplists category.
async def handleTopLists():
    res = spotify.category_playlists("toplists", limit=1)
    playlistIds = [i["id"] for i in res["playlists"]["items"]]
    await asyncio.gather(*[handlePlaylist(playlist) for playlist in playlistIds])


# Get tracks in playlist.
async def handlePlaylist(playlistId: str):
    res = spotify.playlist_tracks(playlistId)
    spotifyTrackData = [i["track"] for i in res["items"]]
    spotifyTracks = [
        SpotifyTrack(track["id"], track["name"], track["artists"][0]["name"])
        for track in spotifyTrackData
    ]
    await asyncio.gather(*[handleSpotifyTrack(track) for track in spotifyTracks])


async def handleSpotifyTrack(spotifyTrack: SpotifyTrack):
    features = await getSpotifyFeatures(spotifyTrack.id)
    tags = getLastFmTags(spotifyTrack.title, spotifyTrack.artist)
    track = Track(spotifyTrack, features, tags)
    print(track)
    allTracks.append(track)


async def getSpotifyFeatures(trackId: str):
    [res] = spotify.audio_features([trackId])
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


def getLastFmTags(title: str, artist: str):
    return list(
        map(lambda x: x.item.name, lastfm.get_track(artist, title).get_top_tags())
    )


if __name__ == "__main__":
    asyncio.run(handleTopLists())
