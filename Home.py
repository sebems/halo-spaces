import streamlit as st
import pandas as pd
from datetime import date
import hashlib
from helpers.constant import BUILDING_NAMES, BOARD_TYPES, TOKEN
from helpers.assets_helper import createSpacesDataframe

# Streamlit Page Configuration
st.set_page_config(
    page_title="Home",
    page_icon="./images/calvin.png",
    layout="wide",  # Use the full width of the browser window
    menu_items={"Get Help": "https://helpdesk.calvin.edu/portal/"},
)


@st.cache_data(ttl=3600)
def load_data():
    """
    Loads space data from a CSV file, preprocesses it, and caches it.

    Returns:
        pandas.DataFrame: Processed DataFrame containing space data.
    """
    df = pd.read_csv("./data/space_data.csv", index_col=0).fillna(0)
    # Convert 'SEAT_COUNT' to integer, handling non-numeric values
    df["SEAT_COUNT"] = (
        pd.to_numeric(df["SEAT_COUNT"], errors="coerce").fillna(0).astype(int)
    )
    # Generate a unique hash for each room name
    df["ROOM_HASH"] = df["ROOM_NAME"].apply(
        lambda x: hashlib.md5(x.encode()).hexdigest()
    )
    return df


def create_sidebar_filters():
    """
    Creates and returns filter selections from the sidebar.

    Returns:
        dict: Dictionary containing filter selections (building, board type, capacity, smart room, teams room).
    """
    with st.sidebar:
        building = st.selectbox("Filter Buildings", BUILDING_NAMES)
        board_type = st.selectbox(
            "Filter Board Types", ["All"] + [bt for bt in BOARD_TYPES if bt != "All"]
        )
        capacity = st.slider("Room Capacity", 0, 200, step=20)

    return {"building": building, "board_type": board_type, "capacity": capacity}


def filter_dataframe(df, filters):
    """
    Filters the DataFrame based on the provided filter selections.

    Args:
        df (pandas.DataFrame): The DataFrame to filter.
        filters (dict): Dictionary containing filter selections.

    Returns:
        pandas.DataFrame: Filtered DataFrame.
    """
    if df.empty:
        return df

    # Select only the necessary columns for filtering and display
    filtered_df = df[
        [
            "Room Name",
            "BUILDING_NAME",
            "SEAT_COUNT",
            "BOARD_TYPE",
            "SMART_CLASSROOM",
            "TEAMS_ROOM",
            "CAMERA_MIC",
            "ETHERNET_JACK",
            "CLASSROOM_TYPE",
            "CAMERA_TYPE",
            "DISPLAY_TYPE",
            "MICROPHONE_TYPE",
            "SCREEN_TYPE",
            "COMPUTER",
            "COMPUTER_LAB",
            "SOUND_SYSTEM",
            "PODIUM_TYPE",
            "RECORD_TYPE",
            "INPUTS",
            "ADDITIONAL_ROOM_SPECS",
            "ROOM_HASH",
        ]
    ].copy()

    # Apply filters
    if filters["building"]:
        filtered_df = filtered_df[filtered_df["BUILDING_NAME"] == filters["building"]]
    if filters["capacity"] > 0:
        filtered_df = filtered_df[filtered_df["SEAT_COUNT"] >= filters["capacity"]]
    if filters["board_type"] != "All":
        filtered_df = filtered_df[filtered_df["BOARD_TYPE"] == filters["board_type"]]

    return filtered_df.sort_values(by=["Room Name"])


def display_table(column, df):
    """
    Displays the DataFrame in a Streamlit table within the specified column.

    Args:
        column (streamlit.delta_generator.DeltaGenerator): The Streamlit column to display the table in.
        df (pandas.DataFrame): The DataFrame to display.
    """
    with column:
        if not df.empty:
            st.dataframe(
                df[["Room Name"]],
                hide_index=True,
                use_container_width=True,
            )
        else:
            st.dataframe(pd.DataFrame(columns=["Room Name"]), use_container_width=True)


def display_status(label, value):
    """
    Displays a success or error message based on the given value.

    Args:
        col (streamlit.delta_generator.DeltaGenerator): The Streamlit column to display the status in.
        label (str): The label for the status.
        value (bool): The boolean value determining success or error.
    """

    if eval(str(value)):
        st.success(label, icon="✅")
    else:
        st.error(label, icon="❌")


def display_room_details(dataframe_in):
    """
    Displays detailed information for each room in the DataFrame.

    Args:
        dataframe_in (pandas.DataFrame): The DataFrame containing room details.
    """
    for _, row in dataframe_in.iterrows():
        with st.expander(row["Room Name"]):
            col_left, col_right = st.columns([1, 3])

            with col_left:
                st.image("./images/seminar.png", width=100)
                with st.popover(f"{row['Room Name']} Details"):
                    if row["BOARD_TYPE"]:
                        st.pills(
                            "Board Type",
                            row["BOARD_TYPE"].split(", "),
                            key=f"board_type_{row['ROOM_HASH']}",
                        )
                    else:
                        st.markdown("Board Type: **None**")

                    st.markdown(
                        f"Display Type: **{row['DISPLAY_TYPE'] if row['DISPLAY_TYPE'] else 'None'}**"
                    )
                    st.markdown(
                        f"Computer Lab: **{row['COMPUTER_LAB'] if row['COMPUTER_LAB'] else 'None'}**"
                    )

            with col_right:
                st.metric(label="Classroom Type", value=row["CLASSROOM_TYPE"])
                st.metric(label="Seat Count", value=row["SEAT_COUNT"])
            st.divider()

            display_status("Camera Mic Available", row["CAMERA_MIC"])


def optimize_spaces_assets(dataframe_in):
    st.logo(image="./images/calvin_banner_black.png")
    st.header("Spaces Assets [Draft]", divider="red")

    table_col, details_col = st.columns([0.5, 3])
    sidebar_filters = create_sidebar_filters()
    filtered_df = filter_dataframe(dataframe_in, sidebar_filters)
    display_table(table_col, filtered_df)

    with details_col:
        if not filtered_df.empty:
            display_room_details(filtered_df)
        else:
            st.info("No rooms match your filter criteria.")


def main():
    weekday = date.today().strftime("%a")

    if weekday == "Sat":
        with st.spinner("Updating spaces data...", show_time=True):
            createSpacesDataframe(TOKEN)

    main_df = load_data()
    main_df.rename(columns={"ROOM_NAME": "Room Name"}, inplace=True)
    optimize_spaces_assets(main_df)


if __name__ == "__main__":
    main()
