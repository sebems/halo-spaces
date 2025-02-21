import requests
import json
import random
import streamlit as st


### API CALL for Token

base_URL = "https://halo.calvin.edu/api"
auth_URL = "https://halo.calvin.edu/auth/token?tenant=calvinuni"
asset_URL = base_URL + "/asset"
CLIENT_ID, CLIENT_SECRET = st.secrets["CLIENT_ID"], st.secrets["CLIENT_SECRET"]

ASSET_GROUP_ID = 103  # asset group id for classrooms

### payload data
data = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "grant_type": "client_credentials",
    "scope": "read:assets edit:assets",
}

### map for Calvin Building Codes (not the full list of what's on campus--just what is in Halo)
building_codes = {
    "Arena Complex Classrooms": "HC",
    "CFAC Classrooms": "CF",
    "Chapel Classrooms": "CP",
    "Commons Annex Classrooms": "CA",
    "DeVos Classrooms": "DC",
    "DeVries Hall Classrooms": "DH",
    "Engineering Building Classrooms": "EB",
    "Hiemenga Hall Classrooms": "HH",
    "North Hall Classrooms": "NH",
    "Science Building Classrooms": "SB",
    "Spoelhof University Center Classrooms": "SC",
}


@st.cache_data  # caches the data to avoid long renders and reruns
def getToken():
    """
    Gets API Token for session. This has read and edit access to assets in Halo ITSM

        @return:
            token: str -- API Token
    """
    response = requests.post(auth_URL, data=data)
    return response.json()["access_token"] if response.ok else ""


@st.cache_data(ttl=None)
def compressFieldsJson(jsonDetails):
    res = {key["id"]: key["display"] for key in jsonDetails}
    return res


@st.cache_data(ttl=None)
def getClassDetails(token, id):

    try:
        if len(token) > 0:  # check if the token is empty

            # Header Authentication
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }

            # query to get all Classroom Assets from Halo
            query = f"/{id}?includediagramdetails=True&includedetails={True}"

            # GET API Call for Classroom Assets
            response = requests.get(url=asset_URL + query, headers=headers)

            assets_resp = response.json()
            jsonDetails = assets_resp["fields"]
            result = compressFieldsJson(jsonDetails)
            # result["key_field"] = assets_resp["key_field"]

            return result if len(assets_resp) > 0 else []
        else:
            raise Exception
    except Exception as err:
        print(err, "Token is empty")


@st.cache_data
def getClassRoomsCondensed(token):
    """
    Gets the list of Classrooms Assets from Halo in a Codensed Dictionary variable

        @returns:
            modi_classes: dict
    """
    ### map for Classroom Assets by their Building Code -- aka Final Result
    modi_classes = {
        "CFAC": [],
        "Chapel": [],
        "Commons Annex": [],
        "DeVos": [],
        "DeVries Hall": [],
        "Engineering Building": [],
        "Hekman Library": [],
        "Hiemenga Hall": [],
        "Hoogenboom Center": [],
        "North Hall": [],
        "Science Building Classrooms": [],
        "Spoelhof Center": [],
        "Van Noord": [],
    }

    try:
        if len(token) > 0:  # check if the token is empty

            # Header Authentication
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }

            # query to get all Classroom Assets from Halo
            query = f"?assetgroup_id={ASSET_GROUP_ID}"

            # GET API Call for Classroom Assets
            response = requests.get(url=asset_URL + query, headers=headers)
            asset_count = response.json()["record_count"]
            classroom_json = response.json()["assets"]

            ### Fills modi_classes dictionary according to building_codes map above
            for classroom in classroom_json:
                # TODO: add check for empty or invalid field
                halo_building_name = classroom["assettype_name"]
                room_name = classroom["inventory_number"]
                room_id = classroom["id"]

                modi_classes[halo_building_name].append([room_name, room_id, []])

            if asset_count != 0:
                return modi_classes
            else:
                return "No Classrooms in the Database"
        else:
            raise Exception
    except Exception as err:
        print(err, "Token is empty")
