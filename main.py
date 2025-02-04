import streamlit as st
import pandas as pd
from assets_helper import getToken, getClassRoomsCondensed
from attachments_helper import getAttachmentsByHaloID, getAttachmentImage

TOKEN = getToken()
HEADERS = ["Room Name", "Room ID", "Room Capacity"]

st.header("Spaces Assets [Draft]")

st.divider()

table_col, details_col = st.columns(2)
config = {"Room ID": st.column_config.NumberColumn("Room ID", format="%d")}


def createClassExpander(room_name: str, room_id: int, room_cap: int, isCrestronAvailable: bool):
    """
    Creates an Expander for each space
    """
    a_expander = st.expander(room_name)

    image = ''
    attachments = getAttachmentsByHaloID(TOKEN, room_id)

    if attachments != None:
        image = getAttachmentImage(TOKEN, attachments[0])
    else:
        image = "./images/seminar.png"

    a_expander.image(image, width=100)
    a_expander.divider()

    col1, col2 = a_expander.columns(2)
    col1.markdown(f"""#### {room_name}""")
    col2.metric(label="Room Capacity", value=room_cap)

    icon = "✅" if isCrestronAvailable else "❌"

    a_expander.info("Crestron Panel Available", icon=icon)


class_dict = getClassRoomsCondensed(TOKEN)

# SIDEBAR SECTION
sidebar = st.sidebar


with sidebar:
    search = st.text_input("Search")
    submit = st.button("Submit", on_click=print(search))
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

capacity_filter = sidebar.slider("Room Capacity", 10, 200, (20, 50))

with table_col:
    building_choice = f"{building_options}" + " Classrooms"

    if building_options != None and len(class_dict) > 0:
        building_rooms = class_dict[building_choice]  # gets the building choice

        # MAIN DATAFRAME OF SPACES ON CAMPUSs
        class_df = pd.DataFrame(building_rooms, columns=HEADERS)

        if search != "":
            class_df = class_df[class_df["Room Name"] == search]

        class_df = class_df[
            class_df["Room Capacity"] >= min(capacity_filter)
        ]  # add room capacity filter

        st.dataframe(
            class_df, column_config=config, use_container_width=True, hide_index=True
        )  # display dataframe
    else:
        st.dataframe(pd.DataFrame())

with details_col:
    for room, room_id, capacity in zip(
        class_df["Room Name"].tolist(), class_df["Room ID"].tolist(), class_df["Room Capacity"].tolist()
    ):
        # apart from the room_name param, the rest are dummy values waiting for change in Halo
        createClassExpander(room, room_id, capacity, True)

    # TODO: get classroom details

    # TODO: link classroom assets to images | need to host images in a different repo

    # TODO: link classrooms to their respective assets
