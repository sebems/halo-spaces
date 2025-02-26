import streamlit as st
import pandas as pd
from helpers.assets_helper import getClassRoomsCondensed
from helpers.attachments_helper import getAttachmentsByHaloID, getAttachmentImage
from helpers.constant import TOKEN, BUILDING_NAMES

st.set_page_config(
    page_title="Gallery",
    page_icon="./images/calvin.png",
    layout="wide",
    menu_items={"Get Help": "https://helpdesk.calvin.edu/portal/"},
)

## Main Logo
MAIN_LOGO = st.logo(image="./images/calvin_banner_black.png")

## Main Header with Divider
MAIN_HEADER = st.header("Gallery", divider="red")

SIDEBAR = st.sidebar
CLASS_DICT = getClassRoomsCondensed(TOKEN)
COL_HEADERS = ["Room Name", "Room ID"]


with SIDEBAR:
    building_options = st.selectbox("Filter Buildings", BUILDING_NAMES)


@st.cache_data(ttl=None)
def imageExpander(room_name: str, room_id: int):
    a_xpndr = st.expander(room_name)
    image = ""
    attachments = getAttachmentsByHaloID(TOKEN, room_id)
    if attachments != None:
        for link in attachments:
            a_xpndr.image(getAttachmentImage(TOKEN, link), width=200)


building_choice = f"{building_options}"

if building_options != None and len(CLASS_DICT) > 0:
    building_rooms = CLASS_DICT[building_choice]  # gets the building choice

    # DATAFRAME COLUMN CONFIGURATION
    config = {"Room ID": st.column_config.NumberColumn("Room ID", format="%d")}

    # MAIN DATAFRAME OF SPACES ON CAMPUSs
    class_df = pd.DataFrame(building_rooms, columns=COL_HEADERS)

    ## STREAMLIT DATAFRAME DISPLAY
    MAIN_DATAFRAME = st.dataframe(
        class_df["Room Name"],  # show only the room names
        column_config=config,
        use_container_width=True,
        hide_index=True,
    )
else:
    ## DISPLAY AN EMPTY DATAFRAME IF THE API QUERY IS EMPTY
    MAIN_DATAFRAME = st.dataframe(pd.DataFrame(columns=COL_HEADERS))

# LOAD CLASS IMAGES
for room, room_id in zip(class_df["Room Name"].tolist(), class_df["Room ID"].tolist()):
    # apart from the room_name param, the rest are dummy values waiting for change in Halo
    imageExpander(room_name=room, room_id=room_id)
