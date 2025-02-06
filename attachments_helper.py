import requests
import streamlit as st

### API CALL for Token

base_URL = "https://halo.calvin.edu/api"
auth_URL = "https://halo.calvin.edu/auth/token?tenant=calvinuni"
asset_URL = base_URL + "/asset"
attach_URL = base_URL + "/attachment"

DEBUG = True


@st.cache_data(allow_output_mutation=True)
def getAttachmentsByHaloID(token, class_id):
    try:
        if len(token) > 0:  # check if the token is empty

            # Header Authentication
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }

            # query to get all Classroom Assets from Halo
            query = f"?type=4&unique_id={class_id}"

            # GET API Call for Classroom Assets
            response = requests.get(url=attach_URL + query, headers=headers)

            attachments_resp = response.json()["attachments"]

            if len(attachments_resp) > 0:
                attachments_resp = [attach["id"] for attach in attachments_resp]
                return attachments_resp
            else:
                []
        else:
            raise Exception
    except Exception as err:
        print(err, "Token is empty")


@st.cache_data(allow_output_mutation=True)
def getAttachmentImage(token, class_id):
    try:
        if len(token) > 0:  # check if the token is empty

            # Header Authentication
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }

            # query to get all Attachments linked to a Classroom Asset from Halo
            query = f"/{class_id}?getToken=true"

            # GET API Call for Classroom Assets
            response = requests.get(url=attach_URL + query, headers=headers)

            attachments_resp = response.json()
            return attachments_resp["link"]

        else:
            raise Exception
    except Exception as err:
        print(err, "Token is empty")
