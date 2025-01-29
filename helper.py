import pandas as pd
import requests, json

### API CALL for Token

base_URL = "https://halo.calvin.edu/api"
auth_URL = "https://halo.calvin.edu/auth/token?tenant=calvinuni"
asset_URL = base_URL + "/asset"
CLIENT_ID = ""
CLIENT_SECRET = ""
ASSET_GROUP_ID = 103 # asset group id for classrooms

data = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "grant_type": "client_credentials",
    "scope": "read:assets edit:assets"
}

def getToken():

    response = requests.post(auth_URL, data=data)
    token = response.json()["access_token"]

    return token

def getClassroomAssets(token):

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    query = "?assetgroup_id={}".format(ASSET_GROUP_ID)

    response = requests.get(url=asset_URL+query, headers=headers)
    asset_count = response.json()["record_count"]
    classroom_json = response.json()["assets"]

    if asset_count != 0:
        return classroom_json
    else:
        return("No Classrooms in the Database")

