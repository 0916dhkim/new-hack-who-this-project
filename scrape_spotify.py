from config import config
from spotipy.oauth2 import SpotifyClientCredentials
import asyncio
import httpx
from typing import List
import os


# Use spotipy package for maanaging access tokens.
if config["spotifyClientId"] is None:
  raise Exception("Environment variable SPOTIFY_CLIENT_ID is required.")
if config["spotifyClientSecret"] is None:
  raise Exception("Environment variable SPOTIFY_CLIENT_SECRET is required.")
spotify = SpotifyClientCredentials(
  client_id=config["spotifyClientId"],
  client_secret=config["spotifyClientSecret"]
)


class Track:
  def __init__(self, id, preview, title, artist):
    self.id = id
    self.preview = preview
    self.title = title
    self.artist = artist

  def __str__(self):
    return f"<[{self.id}] {self.title} ; {self.artist}>"


# All tracks.
allTracks: List[Track] = []


# Get playlists from toplists category.
async def handleTopLists():
  async with httpx.AsyncClient() as client:
    res = await client.get(
      "https://api.spotify.com/v1/browse/categories/toplists/playlists?limit=50",
      headers={
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer " + spotify.get_access_token(as_dict=False)
      }
    )
    playlistIds = [i["id"] for i in res.json()["playlists"]["items"]]
  await asyncio.gather(*[handlePlaylist(playlist) for playlist in playlistIds])


# Get tracks in playlist.
async def handlePlaylist(playlistId: str) -> List[Track]:
  async with httpx.AsyncClient() as client:
    res = await client.get(
      f"https://api.spotify.com/v1/playlists/{playlistId}/tracks",
      headers={
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer " + spotify.get_access_token(as_dict=False)
      }
    )
    trackData = [i["track"] for i in res.json()["items"]]
  tracks = [ Track(track["id"], track["preview_url"], track["name"], track["artists"][0]["name"]) for track in trackData ]
  await asyncio.gather(*[handleTrack(track) for track in tracks])

async def handleTrack(track: Track):
  allTracks.append(track)


asyncio.run(handleTopLists())
