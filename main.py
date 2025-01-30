import streamlit as st
import pandas as pd
from helper import getToken, getClassRoomsCondensed

TOKEN = getToken()
HEADERS = ["Room ID", "Building Code", "Room Name"]

st.header("Spaces Assets [Draft]")

# TODO: setup page navigation
class_dict = getClassRoomsCondensed(TOKEN)

# column config for data frame
config = {"Room ID": st.column_config.TextColumn()}

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

building_choice = f"{building_options}" + " Classrooms"

if building_options != None:
    arena_rooms = class_dict[building_choice]
    class_df = pd.DataFrame(arena_rooms, columns=HEADERS)

    st.dataframe(class_df, column_config=config, use_container_width=True)
else:
    st.dataframe(pd.DataFrame())

expander = st.expander("Test Classroom")

expander.image("./images/seminar.png", width=100)
expander.divider()

col1, col2, col3 = expander.columns(3)
col1.metric(label="Room Capacity", value=100)
col2.metric(label="Room Capacity", value=100)
col3.metric(label="Room Capacity", value=100)
expander.info("Crestron Panel Available", icon="✅")

# TODO: make the classroom assets displayable via model components or cards

# TODO: add filter mechanic

# TODO: add search bar

# TODO: link classroom assets to images

# TODO: link classrooms to their respective assets
