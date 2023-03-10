from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import uvicorn
from urllib.request import urlopen
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import Body
from dotenv import load_dotenv
from urllib.parse import urlencode
import os
import requests
import urllib
import mysql.connector as mysql
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import bcrypt

app = FastAPI()
load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
# db_host = os.getenv('MYSQL_HOST')
# db_user = os.getenv('MYSQL_USER')
# db_pass = os.getenv('MYSQL_PASSWORD')
# db_name = os.getenv('MYSQL_DATABASE')

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
    return access_token

def authenticate_user(username:str, password:str) -> bool:
    return db.check_user_password(username, password)

def create_user(first_name:str, last_name:str, username:str, password:str) -> int:
  password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

  db = mysql.connect(**db_config)
  cursor = db.cursor()
  query = "insert into users (first_name, last_name, username, password) values (%s, %s, %s, %s)"
  values = (first_name, last_name, username, password)
  cursor.execute(query, values)
  db.commit()
  db.close()
  return cursor.lastrowid

@app.get("/", response_class=HTMLResponse)
async def get_html() -> HTMLResponse:
    with open("index.html") as html:
        return HTMLResponse(content=html.read())

@app.get("/register", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
    with open("register.html") as html:
        return HTMLResponse(content=html.read())

@app.get("/play", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
    with open("play.html") as html:
        return HTMLResponse(content=html.read())

@app.get("/play1", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
    with open("play1.html") as html:
        return HTMLResponse(content=html.read())

@app.get("/sign-in")
async def auth():
    scope = ["playlist-modify-private", "playlist-modify-public"]
    auth_url = f"https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={' '.join(scope)}"
    return HTMLResponse(content=f'<a href="{auth_url}">Authorize</a>')


@app.get("/search/{item:path}")
async def search(item: str):
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0"})
    global headers
    toSend = {'spotify': {}, 'soundcloud': {}}
    params = {
        'q': item,
        'type': 'track',
        'limit': 5
    }
    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    answer = response.json()
    for i in range(0, len(answer['tracks']['items'])) :
        toSend['spotify'].update({i: {'link': answer['tracks']['items'][i]['uri'], 'artist': answer['tracks']['items'][i]['artists'][0]['name'], 'title': answer['tracks']['items'][i]['name']}})
    soundcloud_id = "VTl9gNS05wF10zfiwKJ6FwK9mJsLVuAV"
    url = "https://api-v2.soundcloud.com/search?q=" + item + "&client_id=" + soundcloud_id
    url = "https://api-v2.soundcloud.com/search?q=" + urllib.parse.quote(item)
    url = url + "&limit=" + urllib.parse.quote("6") + "&client_id=" + urllib.parse.quote(soundcloud_id)
    responseSoundCloud = session.get(url)
    answerSoundCloud = responseSoundCloud.json()
    for c in range(0, len(answerSoundCloud['collection'])-1):
        link = answerSoundCloud['collection'][c]['uri']
        if answerSoundCloud['collection'][c]['user'] != None:
            artist = answerSoundCloud['collection'][c]['user']['username']
        else:
            artist = 'none'
        title = answerSoundCloud['collection'][c]['title']
        toSend['soundcloud'].update( {c: {'link': link, 'artist': artist, 'title': title}})
    toSend.update({"spotify_token": access_token})
    return toSend

@app.get("/user/spotify_credential")
async def get_credential():
    print(access_token)
    return JSONResponse({"spotify_token": access_token})

@app.get("/callback")
async def callback(code):
    access_token = get_access_token(code)
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get("https://api.spotify.com/v1/me", headers=headers)
    return RedirectResponse(url='/', headers={'token': access_token})


@app.post("/createUsers/")
async def create_user(username: str = Body(...), password: str= Body(...)):
    db = mysql.connect(host=db_host, user=db_user, password=db_pass)
    
    cursor = db.cursor()
    cursor.execute('USE onespot')
    try:
        cursor.execute("select * from users where username=%s", (username,))
        if not cursor.rowcount:
            try:
                cursor.execute("insert into users (username, password) values (%s, %s);", (username, password))
                cursor.execute('''create table %s (
                    song_id integer  AUTO_INCREMENT PRIMARY KEY,
                    link VARCHAR(300) NOT NULL, 
                    tite VARCHAR(300) NOT NULL, 
                    artist VARCHAR(300) NOT NULL);''', (username,))
                db.commit()
                db.close()
                return JSONResponse(status_code=200, content={"message": "User added sucessfully!"})
            except RuntimeError as err:
                db.close()
                return JSONResponse(status_code=409, content={"message":"User addition failed!", 'error':err})
        else:
            return JSONResponse(status_code=418, content={"message": "I'm a teapot"})
    except RuntimeError as err:
        db.close()
        return JSONResponse(status_code=409, content={"message":"User addition failed!", 'error':err})
    

@app.post("/addPlaylist/")
async def add_playlist(link: str = Body(...), title: str = Body(...), artist: str = Body(...)):
    db = mysql.connect(host=db_host, user=db_user, password=db_pass)
    cursor = db.cursor()
    cursor.execute('USE OneSpot')
    try:
        cursor.execute("select * from orders where order_id=%s;", (order_id,))
        db.commit()
        db.close()
        return JSONResponse(status_code=200, content={"message": "Order status changed!"})
    except RuntimeError as err:
        db.close()
        return JSONResponse(status_code=409, content={"message":"Query Failed!", 'error':err})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6543)