import streamlit as st
import pandas as pd
from assets_helper import getToken, getClassRoomsCondensed
from attachments_helper import getAttachmentsByHaloID, getAttachmentImage

#######  PAGE CONFIG AND LOGO  #######
st.set_page_config(
    page_title="Halo Spaces' Assets",
    page_icon="./images/calvin.png",
    layout="wide",
    menu_items={"Get Help": "https://helpdesk.calvin.edu/portal/"},
)

## Main Logo
st.logo(image="./images/calvin_banner_black.png")

## Main Header with Divider
st.header("Spaces Assets [Draft]", divider="red")

## PAGE COLUMNS
table_col, details_col = st.columns([1, 3])  # the details_col has more space allotted

TOKEN = getToken()
COL_HEADERS = ["Room Name", "Room ID", "Room Capacity"]


@st.cache_data(ttl = None)
def createClassExpander(
    room_name: str, room_id: int, room_cap: int, isCrestronAvailable: bool
):
    """
    Creates an Expander for each space
    """
    a_expander = st.expander(room_name)

    attachments = getAttachmentsByHaloID(TOKEN, room_id)

    if attachments != None:
        # i = st.columns(len(attachments))
        for link in attachments:
            a_expander.image(getAttachmentImage(TOKEN, link), width=100)
    else:
        a_expander.image("./images/seminar.png", width=100)

    a_expander.divider()

    col1, col2 = a_expander.columns(2)
    col1.markdown(f"""#### {room_name}""")
    col2.metric(label="Room Capacity", value=room_cap)

    icon = "✅" if isCrestronAvailable else "❌"

    a_expander.info("Crestron Panel Available", icon=icon)


class_dict = getClassRoomsCondensed(TOKEN)

# SIDEBAR SECTION
sidebar = st.sidebar


## DUMMY FUNCTION FOR SEARCH BTN
def fiz():
    pass


with sidebar:
    search = st.text_input("Search")
    submit = st.button("Submit", on_click=fiz)
    building_options = st.selectbox(
        "Filter Buildings",
        (
            "Arena Complex",
            "CFAC",
            "Chapel",
            "Commons Annex",
            "DeVos",
            "DeVries Hall",
            "Engineering Building",
            "Hiemenga Hall",
            "North Hall",
            "Science Building",
            "Spoelhof University Center",
        ),
    )

capacity_filter = sidebar.slider("Room Capacity", 10, 200, step=10)

with table_col:
    building_choice = f"{building_options}" + " Classrooms"

    if building_options != None and len(class_dict) > 0:
        building_rooms = class_dict[building_choice]  # gets the building choice

        # DATAFRAME COLUMN CONFIGURATION
        config = {"Room ID": st.column_config.NumberColumn("Room ID", format="%d")}

        # MAIN DATAFRAME OF SPACES ON CAMPUSs
        class_df = pd.DataFrame(building_rooms, columns=COL_HEADERS)

        if search != "":
            class_df = class_df[class_df["Room Name"] == search]

        class_df = class_df[
            class_df["Room Capacity"] >= capacity_filter
        ]  # add room capacity filter

        ## STREAMLIT DATAFRAME DISPLAY
        st.dataframe(
            class_df["Room Name"],  # show only the room names
            column_config=config,
            use_container_width=True,
            hide_index=True,
        )
    else:
        ## DISPLAY AN EMPTY DATAFRAME IF THE API QUERY IS EMPTY
        st.dataframe(pd.DataFrame(columns=COL_HEADERS))

with details_col:
    for room, room_id, capacity in zip(
        class_df["Room Name"].tolist(),
        class_df["Room ID"].tolist(),
        class_df["Room Capacity"].tolist(),
    ):
        # apart from the room_name param, the rest are dummy values waiting for change in Halo
        createClassExpander(room, room_id, capacity, True)

    # TODO: get classroom details

    # TODO: link classrooms to their respective assets
