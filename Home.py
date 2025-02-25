import streamlit as st
import pandas as pd
import random, string

from assets_helper import (
    getToken,
    getClassRoomsCondensed,
    getClassDetails,
    BUILDING_NAMES,
)

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
COL_HEADERS = ["Room Name", "Room ID"]
CLASS_DICT = getClassRoomsCondensed(TOKEN)
SIDEBAR = st.sidebar # SIDEBAR SECTION

def genRandKey():

    # https://stackoverflow.com/questions/367586/generating-random-text-strings-of-a-given-pattern
    digits = ''.join(random.sample(string.digits, 8))
    chars = ''.join(random.sample(string.ascii_letters, 15))
    return f"{digits}_{chars}"

def dummyEntry(room_name, room_id: int):
    spaceDetails = getClassDetails(TOKEN, room_id)

    if spaceDetails != None:
        test_expander = st.expander(room_name)

        test_expander.image("./images/seminar.png", width=100)

        test_expander.divider()

        col1, col2 = test_expander.columns(2)

        classType = spaceDetails[182]
        col1.metric(label="Classroom Type", value=classType)
        roomCap = spaceDetails[180]
        col2.metric(label="Seat Count", value=roomCap)

        isCrestronAvailable = True if spaceDetails[201] == "True" else False
        isTeamsRoom = True if spaceDetails[204] == "True" else False

        crestronIcon = "✅" if isCrestronAvailable else "❌"
        teamsIcon = "✅" if isTeamsRoom else "❌"

        if isCrestronAvailable:
            test_expander.success("Smart Room", icon=crestronIcon)
        else:
            test_expander.error("Smart Room", icon=crestronIcon)

        if isTeamsRoom:
            test_expander.success("Teams Room", icon=teamsIcon)
        else:
            test_expander.error("Teams Room", icon=teamsIcon)

        with test_expander.popover("View More Details"):
            col, col2 = st.columns([3, 1])

            with col:
                st.markdown(f"Board Type: **{spaceDetails[184]}**")
                st.markdown(f"Camera Type: **{spaceDetails[181]}**")
                st.markdown(f"Display Type: **{spaceDetails[200]}**")
                st.markdown(f"Microphone Type: **{spaceDetails[198]}**")

                st.markdown(f"Screen Type: **{spaceDetails[190]}**")
                st.markdown(f"Computer: **{spaceDetails[196]}**")
                st.markdown(f"Computer Lab: **{spaceDetails[195]}**")
                st.markdown(f"Sound System: **{spaceDetails[202]}**")
            with col2:
                if spaceDetails[188] != "None":
                    st.pills("Podium Type", spaceDetails[188].split(", "), key=genRandKey())
                else:
                    st.markdown(f"Podium Type: **{spaceDetails[188]}**")

                if spaceDetails[195] != "None":
                    st.pills("Record Type", spaceDetails[195].split(", "), key=genRandKey())
                else:
                    st.markdown(f"Podium Type: **{spaceDetails[195]}**")

                if spaceDetails[199] != "None":
                    st.pills("Inputs", spaceDetails[199].split(", "), key=genRandKey())
                else:
                    st.markdown(f"Inputs: **{spaceDetails[199]}**")

                if spaceDetails[203] != "None":
                    st.pills("Additional Room Specs", spaceDetails[203].split(", "), key=genRandKey())
                else:
                    st.markdown(f"Additional Room Specs: **{spaceDetails[203]}**")

with SIDEBAR:
    building_options = st.selectbox("Filter Buildings", BUILDING_NAMES)
    cap_filter = SIDEBAR.slider("Room Capacity", 10, 200, step=10)


with table_col:
    building_choice = f"{building_options}"

    if building_options != None and len(CLASS_DICT) > 0:
        building_rooms = CLASS_DICT[building_choice]  # gets the building choice

        # DATAFRAME COLUMN CONFIGURATION
        config = {"Room ID": st.column_config.NumberColumn("Room ID", format="%d")}

        # MAIN DATAFRAME OF SPACES ON CAMPUSs
        class_df = pd.DataFrame(building_rooms, columns=COL_HEADERS)

        # # TODO:
        # class_df = class_df[
        #     class_df["Room Capacity"] >= capacity_filter
        # ]  # add room capacity filter

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
    # with st.spinner("Loading Classes", show_time=True):
    for room, room_id in zip(
        class_df["Room Name"].tolist(),
        class_df["Room ID"].tolist()
    ):
        # apart from the room_name param, the rest are dummy values waiting for change in Halo
        dummyEntry(room_name=room, room_id=room_id)
