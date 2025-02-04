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
DEBUG = False

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


def getToken():
    """
    Gets API Token for session. This has read and edit access to assets in Halo ITSM

        @return:
            token: str -- API Token
    """
    response = requests.post(auth_URL, data=data)
    return response.json()["access_token"] if response.ok else ""


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
            return assets_resp if len(assets_resp) > 0 else []
        else:
            raise Exception
    except Exception as err:
        print(err, "Token is empty")


def getClassrooms(token):
    """
    Gets the list of Classrooms from Halo in Dictionary variable

        @returns:
            classroom_json: dict
    """

    try:
        if len(token) > 0:  # check if the token is empty

            # Header Authentication
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }

            # query to get all Classroom Assets from Halo
            query = "?assetgroup_id={}".format(ASSET_GROUP_ID)

            # GET API Call for Classroom Assets
            response = requests.get(url=asset_URL + query, headers=headers)
            asset_count = response.json()["record_count"]
            classroom_json = response.json()["assets"]

            if asset_count != 0:  # check so that we don't have to waste operation time
                return classroom_json
            else:
                return "No Classrooms in the Database"
        else:
            raise Exception
    except Exception as err:
        print(err, "Token is empty")


def getClassRoomsCondensed(token):
    """
    Gets the list of Classrooms Assets from Halo in a Codensed Dictionary variable

        @returns:
            modi_classes: dict
    """

    if DEBUG:
        random.seed(1234)

    ### map for Classroom Assets by their Building Code -- aka Final Result
    modi_classes = {
        "Arena Complex Classrooms": [],
        "CFAC Classrooms": [],
        "Chapel Classrooms": [],
        "Commons Annex Classrooms": [],
        "DeVos Classrooms": [],
        "DeVries Hall Classrooms": [],
        "Engineering Building Classrooms": [],
        "Hiemenga Hall Classrooms": [],
        "North Hall Classrooms": [],
        "Science Building Classrooms": [],
        "Spoelhof University Center Classrooms": [],
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
                halo_building_name = classroom["assettype_name"]
                room_name = classroom["inventory_number"]
                room_id = classroom["id"]

                # TODO: fields to add to halo classroom assets
                # room assets
                # room capacity
                # crestron availability


                modi_classes[halo_building_name].append(
                    [
                        room_name,
                        room_id,
                        random.randint(10, 200),
                    ]  # randint there for testing cap filter
                )

            if asset_count != 0:
                return modi_classes
            else:
                return "No Classrooms in the Database"
        else:
            raise Exception
    except Exception as err:
        print(err, "Token is empty")


### TESTING JSON STRUCTURE
if DEBUG:
    asset_test = getClassDetails(getToken(), "4814")
    with open("./test.json", "w+") as file:
        json.dump(asset_test, file)
