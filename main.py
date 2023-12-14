from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

#loads variables for for my CLIENT_ID and CLIENT_secret from my .env
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
#function responsible for getting my access token
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    #sets url for spotify's token endpoint
    url = "https://accounts.spotify.com/api/token"
    #constructs header required for POST request to to the spotify web api
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    #sets grant type to client_credentials for post request
    data = {"grant_type": "client_credentials"}
    #sends post reqeust to spotify api with url, headers and data 
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    #extracts access token from JSON response
    token = json_result["access_token"]
    return token

#creates a header needed for all spotify api requests
#using my created access token
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}
#/search function taking track input
def search_for_track(token, track):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={track}&type=track&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result= json.loads(result.content)["tracks"]["items"]
    if len(json_result) == 0:
        return None
    return json_result[0]

token = get_token()
#"Bad blood song name used for /search"
result = search_for_track(token, "Bad blood")
print(result)

