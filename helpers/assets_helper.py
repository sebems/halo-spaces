import requests
import streamlit as st
import pandas as pd
# from constant import HEADER_COLS

HEADER_COLS = [
    "CLASSROOM_TYPE",
    "DISPLAY_TYPE",
    "CPT",
    "SEAT_COUNT",
    "TEAMS_ROOM",
    "LAST_REFRESH",
    "LCR_PRICE",
    "LCR_YEAR",
    "CAMERA_TYPE",
    "TIERED_SEATING",
    "SMART_CLASSROOM",
    "DESK_TYPE",  # 186
    "TABLE_TYPE",  # 191
    "BOARD_TYPE",
    "PODIUM_TYPE",
    "SCREEN_TYPE",
    "RECORD_TYPE",
    "COMPUTER_LAB",
    "COMPUTER",
    "CAMERA_MIC",
    "MICROPHONE_TYPE",
    "INPUTS",
    "DISPLAY_TYPE",
    "ETHERNET_JACK",
    "SOUND_SYSTEM",
    "ADDITIONAL_ROOM_SPECS",
    "ROOM_ID",
    "ROOM_NAME",
    "BUILDING_NAME",
]
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


@st.cache_data(ttl="12h")  # caches the data to avoid long renders and reruns
def getToken():
    """
    Gets API Token for session. This has read and edit access to assets in Halo ITSM

        @return:
            token: str -- API Token
    """
    response = requests.post(auth_URL, data=data)
    return response.json()["access_token"] if response.ok else ""


def compressFieldsJson(jsonDetails):
    res = [key["display"] if "display" in key else "None" for key in jsonDetails]
    return res


@st.cache_data
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
            result.append(assets_resp["id"])
            result.append(assets_resp["inventory_number"])
            result.append(assets_resp["assettype_name"])

            return result if len(assets_resp) > 0 else []
        else:
            raise Exception
    except Exception as err:
        print(err)


@st.cache_resource
def createSpacesDataframe(token):
    try:
        if len(token) > 0:  # check if the token is empty

            # Header Authentication
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }

            # query to get all Classroom Assets from Halo
            query = f"?assetgroup_id={ASSET_GROUP_ID}&idonly=True"

            # GET API Call for Classroom Assets
            response = requests.get(url=asset_URL + query, headers=headers)
            space_assets = response.json()["assets"]

            ### GET HALO SPACES BY ID ONLY
            space_assets_ids = [space["id"] for space in space_assets]

            ### GET HALO ROOM DETAILS
            results = [
                getClassDetails(token, space_id) for space_id in space_assets_ids
            ]

            ### RENDER INTO DATAFRAME
            df = pd.DataFrame(
                results,
                columns=HEADER_COLS,
            )

            df.to_csv("./data/space_data.csv")
        else:
            raise Exception
    except Exception as e:
        print(e)
        return []
