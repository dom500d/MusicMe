from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import uvicorn
from urllib.request import urlopen
import json
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import re
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import Body
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from urllib.parse import urlencode
import base64
import webbrowser
import os
import requests
import urllib


load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = "http://localhost:6543/callback"
headers = {}
access_token = ""
app = FastAPI()
app.mount("/public", StaticFiles(directory="public"), name="public")
def get_access_token(auth_code: str):
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": redirect_uri,
        },
        auth=(client_id, client_secret),
    )
    global access_token
    access_token = response.json()["access_token"]
    global headers
    headers = {"Authorization": "Bearer " + access_token}
    print(response.json()["access_token"])
    print(headers)
    return access_token


@app.get("/", response_class=HTMLResponse)
async def get_html() -> HTMLResponse:
    with open("index.html") as html:
        return HTMLResponse(content=html.read())


@app.get("/play", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
    with open("play.html") as html:
        return HTMLResponse(content=html.read())


@app.get("/sign-in")
async def auth():
    scope = ["playlist-modify-private", "playlist-modify-public"]
    auth_url = f"https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={' '.join(scope)}"
    return HTMLResponse(content=f'<a href="{auth_url}">Authorize</a>')


@app.get("/search/{item:path}")
async def search(item: str):
    # global headers
    # print(headers)
    toSend = {}
    # params = {
    #     'q': item,
    #     'type': 'track',
    #     'limit': 5
    # }
    # response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    # answer = response.json()
    # for i in range(0, len(answer['tracks']['items'])) :
    #     toSend.update({i: {'link': answer['tracks']['items'][i]['external_urls']['spotify'], 'artist': answer['tracks']['items'][i]['artists'][0]['name'], 'song': answer['tracks']['items'][i]['name']}})
    soundcloud_id = "VTl9gNS05wF10zfiwKJ6FwK9mJsLVuAV"
    paramsSoundCloud = {
        'q': item,
        'limit': 5,
        'client_id': soundcloud_id
    }    
    url = "https://api-v2.soundcloud.com/search?q=" + item + "&client_id=" + soundcloud_id
    url = "https://api-v2.soundcloud.com/search?q=" + urllib.parse.quote(item)
    url = url + "&limit=" + urllib.parse.quote("5") + "&client_id=" + urllib.parse.quote(soundcloud_id)
    responseSoundCloud = requests.get(url)
    answerSoundCloud = responseSoundCloud.json()
    print(answerSoundCloud['collection'])
    for c in range(0, len(answerSoundCloud['collection'])):
        toSend.update( {i: {'link': answerSoundCloud['collection'][i]['uri'], 'artist': answerSoundCloud['collection'][i]['publisher_metadata']['artist'], 'title': answerSoundCloud['collection'][i]['title']}})
    
    toSend = {'soundCloud': toSend}
    return toSend



@app.get("/callback")
async def callback(code):
    access_token = get_access_token(code)
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get("https://api.spotify.com/v1/me", headers=headers)
    return RedirectResponse(url='/', headers={'token': access_token})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6543)


# name = "Name of your playlist"
# description = "Description of your playlist"

# params = {
#     "name": name,
#     "description": description,
#     "public": True,
# }

# url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
# response = requests.post(url=url, headers=headers, json=params)
# playlist_id = response.json()["id"]

# track_uri = "spotify:track:319eU2WvplIHzjvogpnNc6"
# response = requests.post(
#     f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
#     headers=headers,
#     json={"uris": [track_uri]},
# )
# if response.status_code == 201:
#     return {"message": "Track added successfully!"}
# else:
#     return {"error": response.json()}