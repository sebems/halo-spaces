import streamlit as st
import pandas as pd
from datetime import date
from helper import getToken, getClassRoomsCondensed

TOKEN = getToken()
HEADERS = ["Room Name", "Room Assets"]

st.header("Spaces Assets [Draft]")

st.divider()

table_col, details_col = st.columns(2)

def createClassExpander(room_name: str, room_cap: int, isCrestronAvailable: bool):
    """
    Creates an Expander for each space
    """
    a_expander = st.expander(room_name)

    a_expander.image("./images/seminar.png", width=100)
    a_expander.divider()

    col1, col2 = a_expander.columns(2)
    col1.markdown(f'''#### {room_name}''')
    col2.metric(label="Room Capacity", value=room_cap)

    icon = '✅' if isCrestronAvailable else '❌'

    a_expander.info("Crestron Panel Available", icon=icon)

class_dict = getClassRoomsCondensed(TOKEN)

# SIDEBAR SECTION
sidebar = st.sidebar
sidebar.text_input("Search")
sidebar.button("Submit")

with sidebar:
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

sidebar.slider("Room Capacity Minimum", 10, 200, 10)

with table_col:
    building_choice = f"{building_options}" + " Classrooms"

    if building_options != None and len(class_dict) > 0:
        building_rooms = class_dict[building_choice]    # gets the building choice

        # MAIN DATAFRAME OF SPACES ON CAMPUSs
        class_df = pd.DataFrame(building_rooms, columns=HEADERS)

        st.dataframe(class_df, use_container_width=True, hide_index=True)    # display dataframe
    else:
        st.dataframe(pd.DataFrame())

with details_col:
    for room in class_df["Room Name"].tolist():
        # apart from the room_name param, the rest are dummy values waiting for change in Halo
        createClassExpander(room, 100, True)

    # TODO: get classroom details

    # TODO: link classroom assets to images | need to host images in a different repo

    # TODO: link classrooms to their respective assets