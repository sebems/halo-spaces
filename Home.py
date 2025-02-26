import streamlit as st
import pandas as pd
import random, string
from helpers.constant import *
from helpers.assets_helper import getClassRoomsCondensed, getClassDetails

#######  PAGE CONFIG AND LOGO  #######
st.set_page_config(
    page_title="Halo Spaces' Assets",
    page_icon="./images/calvin.png",
    layout="wide",
    menu_items={"Get Help": "https://helpdesk.calvin.edu/portal/"},
)

## Main Logo
MAIN_LOGO = st.logo(image="./images/calvin_banner_black.png")

## Main Header with Divider
MAIN_HEADER = st.header("Spaces Assets [Draft]", divider="red")

## PAGE COLUMNS
TABLE_COL, DETAILS_COL = st.columns([1, 3])  # the details_col has more space allotted

COL_HEADERS = ["Room Name", "Room ID"]
CLASS_DICT = getClassRoomsCondensed(TOKEN)
SIDEBAR = st.sidebar  # SIDEBAR SECTION


def genRandKey():
    """
    Used to generate unique keys for components (this is to avoid a duplication error)

    Source: https://stackoverflow.com/questions/367586/generating-random-text-strings-of-a-given-pattern
    """
    digits = "".join(random.sample(string.digits, 8))
    chars = "".join(random.sample(string.ascii_letters, 15))
    return f"{digits}_{chars}"


def dummyEntry(room_name, room_id: int):
    """
    Container Template for Room Details
    """
    spaceDetails = getClassDetails(TOKEN, room_id)

    if spaceDetails != None:
        test_expander = st.expander(room_name)
        test_expander.image("./images/seminar.png", width=100)

        test_expander.divider()

        col1, col2 = test_expander.columns(2)

        classType = spaceDetails[CLASSROOM_TYPE]
        col1.metric(label="Classroom Type", value=classType)

        roomCap = spaceDetails[SEAT_COUNT]
        col2.metric(label="Seat Count", value=roomCap)

        isCrestronAvailable = True if spaceDetails[SMART_CLASSROOM] == "True" else False
        isTeamsRoom = True if spaceDetails[TEAMS_ROOM] == "True" else False
        isCamMicPresent = True if spaceDetails[CAMERA_MIC] == "True" else False
        isEthernetPresent = True if spaceDetails[ETHERNET_JACKS] == "True" else False

        crestronIcon = "✅" if isCrestronAvailable else "❌"
        teamsIcon = "✅" if isTeamsRoom else "❌"
        camMicIcon = "✅" if isCamMicPresent else "❌"
        ethernetIcon = "✅" if isEthernetPresent else "❌"

        ### IS CRESTRON AVAILABLE
        if isCrestronAvailable:
            test_expander.success("Smart Room", icon=crestronIcon)
        else:
            test_expander.error("Smart Room", icon=crestronIcon)

        ### IS THIS A TEAMS ROOM
        if isTeamsRoom:
            test_expander.success("Teams Room", icon=teamsIcon)
        else:
            test_expander.error("Teams Room", icon=teamsIcon)

        ### IS A CAMERA MIC AVAILABLE
        if isCamMicPresent:
            test_expander.success("Camera Mic Available", icon=camMicIcon)
        else:
            test_expander.error("Camera Mic Available", icon=camMicIcon)

        ### IS ETHERNET AVAILABLE
        if isEthernetPresent:
            test_expander.success("Ethernet Available", icon=ethernetIcon)
        else:
            test_expander.error("Ethernet Available", icon=ethernetIcon)

        ### DETAILS DROPDOWN
        with test_expander.popover("View More Details"):
            col, col2 = st.columns([3, 2])

            with col:
                st.markdown(f"Board Type: **{spaceDetails[BOARD_TYPE]}**")
                st.markdown(f"Camera Type: **{spaceDetails[CAMERA_TYPE]}**")
                st.markdown(f"Display Type: **{spaceDetails[DISPLAY_TYPE]}**")
                st.markdown(f"Microphone Type: **{spaceDetails[MICROPHONE_TYPE]}**")

                st.markdown(f"Screen Type: **{spaceDetails[SCREEN_TYPE]}**")
                st.markdown(f"Computer: **{spaceDetails[COMPUTER]}**")
                st.markdown(f"Computer Lab: **{spaceDetails[COMPUTER_LAB]}**")
                st.markdown(f"Sound System: **{spaceDetails[SOUND_SYSTEM]}**")

            with col2:
                ### PODIUM TYPE
                if spaceDetails[PODIUM_TYPE] != "None":
                    st.pills(
                        "Podium Type",
                        spaceDetails[PODIUM_TYPE].split(", "),
                        key=genRandKey(),
                    )
                else:
                    st.markdown(f"Podium Type: **{spaceDetails[PODIUM_TYPE]}**")

                ### RECORD TYPE
                if spaceDetails[RECORD_TYPE] != "None":
                    st.pills(
                        "Record Type",
                        spaceDetails[RECORD_TYPE].split(", "),
                        key=genRandKey(),
                    )
                else:
                    st.markdown(f"Record Type: **{spaceDetails[RECORD_TYPE]}**")

                ### INPUTS
                if spaceDetails[INPUTS] != "None":
                    st.pills(
                        "Inputs", spaceDetails[INPUTS].split(", "), key=genRandKey()
                    )
                else:
                    st.markdown(f"Inputs: **{spaceDetails[INPUTS]}**")

                ### ADDITIONAL ROOM SPECS
                if spaceDetails[ADDITIONAL_ROOM_SPECS] != "None":
                    st.pills(
                        "Additional Room Specs",
                        spaceDetails[ADDITIONAL_ROOM_SPECS].split(", "),
                        key=genRandKey(),
                    )
                else:
                    st.markdown(
                        f"Additional Room Specs: **{spaceDetails[ADDITIONAL_ROOM_SPECS]}**"
                    )


with SIDEBAR:
    building_options = st.selectbox("Filter Buildings", BUILDING_NAMES)
    cap_filter = SIDEBAR.slider("Room Capacity", 10, 200, step=10)


with TABLE_COL:
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

with DETAILS_COL:
    for room, room_id in zip(
        class_df["Room Name"].tolist(), class_df["Room ID"].tolist()
    ):
        dummyEntry(room_name=room, room_id=room_id)
