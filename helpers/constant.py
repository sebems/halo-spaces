from helpers.assets_helper import getToken
import random, string

SEAT_COUNT = 180
CAMERA_TYPE = 181
CLASSROOM_TYPE = 182
TIERED_SEATING = 183
BOARD_TYPE = 184
TEAMS_ROOM = 187
PODIUM_TYPE = 188
RECORD_TYPE = 189

SCREEN_TYPE = 190
COMPUTER_LAB = 195
COMPUTER = 196
CAMERA_MIC = 197
MICROPHONE_TYPE = 198
INPUTS = 199

DISPLAY_TYPE = 200
ETHERNET_JACKS = 201
SOUND_SYSTEM = 202
ADDITIONAL_ROOM_SPECS = 203
SMART_CLASSROOM = 204

TOKEN = getToken()

### map for Calvin Building Codes (not the full list of what's on campus--just what is in Halo)
BUILDING_NAMES = [
    "Bunker Interpretive Center",
    "CFAC",
    "Chapel",
    "Commons",
    "Commons Annex",
    "DeVos",
    "DeVries Hall",
    "Engineering Building",
    "Hekman Library",
    "Hiemenga Hall",
    "Hoogenboom Center",
    "Huizenga Track Center",
    "Knollcrest",
    "North Hall",
    "Science Building",
    "Spoelhof Center",
    "Van Noord",
]

BOARD_TYPES = [
    "Chalkboard - Small",
    "Chalkboard - Large",
    "Smart Board",
    "Tack Board",
    "Whiteboard - Large",
    "Whiteboard - Small",
    "None",
]

HEADER_COLS = [
    "CLASSROOM_TYPE",
    "DISPLAY_TYPE",
    "CPT",
    "SEAT_COUNT",
    "TEAMS_ROOM",
    "LAST_REFRESH",
    "LCR_PRICE",
    "LCR_YEAR",
    "CAMERA_TYPE",
    "TIERED_SEATING",
    "SMART_CLASSROOM",
    "DESK_TYPE",  # 186
    "TABLE_TYPE",  # 191
    "BOARD_TYPE",
    "PODIUM_TYPE",
    "SCREEN_TYPE",
    "RECORD_TYPE",
    "COMPUTER_LAB",
    "COMPUTER",
    "CAMERA_MIC",
    "MICROPHONE_TYPE",
    "INPUTS",
    "DISPLAY_TYPE",
    "ETHERNET_JACK",
    "SOUND_SYSTEM",
    "ADDITIONAL_ROOM_SPECS",
    "ROOM_ID",
    "ROOM_NAME",
    "BUILDING_NAME",
]
