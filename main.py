import streamlit as st
import pandas as pd
from assets_helper import getToken, getClassRoomsCondensed, getClassDetails
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


@st.cache_data(ttl=None)
def createClassExpander(
    room_name: str, room_id: int, room_cap, isCrestronAvailable: bool
):
    """
    Creates an Expander for each space
    """
    a_expander = st.expander(room_name)

    attachments = getAttachmentsByHaloID(TOKEN, room_id)

    # if attachments != None:
    #     # i = st.columns(len(attachments))
    #     for link in attachments:
    #         a_expander.image(getAttachmentImage(TOKEN, link), width=100)
    # else:
    a_expander.image("./images/seminar.png", width=100)

    a_expander.divider()

    col1, col2 = a_expander.columns(2)
    col1.markdown(f"""#### {room_name}""")
    col2.metric(label="Room Capacity", value=0)

    icon = "✅" if isCrestronAvailable else "❌"

    a_expander.info("Crestron Panel Available", icon=icon)


def dummyEntry():
    spaceDetails = getClassDetails(TOKEN, 4731)
    test_expander = st.expander("CF222")

    # attachments = getAttachmentsByHaloID(TOKEN, 4731)

    # if attachments != None:
    #     # i = st.columns(len(attachments))
    #     for link in attachments:
    #         test_expander.image(getAttachmentImage(TOKEN, link), width=100)
    # else:
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

    st.write(spaceDetails)
    # with test_expander.popover("View More Details"):
    #     st.pills("Details", spaceDetails.values())


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
            "CFAC",
            "Chapel",
            "Commons Annex",
            "DeVos",
            "DeVries Hall",
            "Engineering Building",
            "Hekman Library",
            "Hiemenga Hall",
            "Hoogenboom Center",
            "North Hall",
            "Science Building Classrooms",
            "Spoelhof Center",
            "Van Noord",
        ),
    )

capacity_filter = sidebar.slider("Room Capacity", 10, 200, step=10)

with table_col:
    building_choice = f"{building_options}"

    if building_options != None and len(class_dict) > 0:
        building_rooms = class_dict[building_choice]  # gets the building choice

        # DATAFRAME COLUMN CONFIGURATION
        config = {"Room ID": st.column_config.NumberColumn("Room ID", format="%d")}

        # MAIN DATAFRAME OF SPACES ON CAMPUSs
        class_df = pd.DataFrame(building_rooms, columns=COL_HEADERS)

        if search != "":
            class_df = class_df[class_df["Room Name"] == search]

        # TODO:
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
    for room, room_id, capacity in zip(
        class_df["Room Name"].tolist(),
        class_df["Room ID"].tolist(),
        class_df["Room Capacity"].tolist(),
    ):
        # apart from the room_name param, the rest are dummy values waiting for change in Halo
        createClassExpander(room, room_id, capacity, True)

    # TODO: get classroom details

    # TODO: link classrooms to their respective assets

######################################################

dummyEntry()
