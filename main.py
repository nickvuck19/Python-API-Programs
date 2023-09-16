# import dotenv to read env file, and import os module, and import base64 to request data, and import json
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json


load_dotenv()

# get client id and client secret

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# request access for spotify data

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers= headers, data=data)
    json_result = json.loads(result.content)
    token =  json_result["access_token"]
    return token


# function to construct header when we need another request

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# function that allows us to search for an artist

def search_for_artist(token, artist_name):
    # url to search for info
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    #query for info we search for, just artist right now
    # If it was artist and track, I would put ...&type=artist,track
    # limit=1 searches for the most popular artist associated w/ artist name
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name found")
        return None

    return json_result[0]

# function to get songs by artist

def get_songs_by_artist(token, artist_id):
    # URL for top tracks by artist
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


token = get_token()
result = search_for_artist(token, "Metallica")
#print(result["name"])
artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)

# for loop to loop thru the songs in a readable format

for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}")



