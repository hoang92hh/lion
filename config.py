"""
Veo 3 Storyboard Station
config.py
"""
from pathlib import Path

# ==========================================================
# Project
# ==========================================================

PROJECT_NAME = "Veo 3 Storyboard Station"
VERSION = "2.0.0"

# ==========================================================
# Folder
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "app.log"

for folder in [DATA_DIR,LOG_DIR]:
    folder.mkdir(parents=True, exist_ok=True)


# ==========================================================
# Scenario Files
# ==========================================================

IMAGE_SCENARIO_FILE = DATA_DIR / "image_scenario.xlsx"
VIDEO_SCENARIO_FILE = DATA_DIR / "video_scenario.xlsx"

SCENARIO_SHEET = "Script"
EXCEL_COLUMNS = {
    "scene_id": 1,
    "template_key": 2,
    "prompt_core": 3,
    "character_list": 4,
    "reference_list": 5,
    "final_prompt": 6,
    "status_time": 7,
    "output_id": 8,
    "file_name": 9,
}



# ==========================================================
# UI
WINDOW_TITLE = PROJECT_NAME
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 850
MIN_WINDOW_WIDTH = 1200
MIN_WINDOW_HEIGHT = 700
# ==========================================================
TREE_COLUMNS = (
    "scene_id",
    "template_key",
    "prompt_core",
    "character_list",
    "reference_list",
    "final_prompt",
    "status_time",
    "output_id",
    "file_name"
)



# Status
STATUS_PENDING = "Pending"
STATUS_RUNNING = "Running"
STATUS_DONE = "Done"
STATUS_ERROR = "Error"
STATUS_SKIP = "Skip"
STATUS_LIST = [STATUS_PENDING, STATUS_RUNNING, STATUS_DONE, STATUS_ERROR, STATUS_SKIP]


# ==========================================================
# Scenario Type
SCENARIO_IMAGE = "IMAGE"
SCENARIO_VIDEO = "VIDEO"
SCENARIO_TYPES = [SCENARIO_IMAGE, SCENARIO_VIDEO]

# Treeview Columns


# # ==========================================================
# # Google Flow Selectors
# # ==========================================================

SELECTORS = {
    # Ô nhập Prompt
    "main_prompt_area":        'div[contenteditable="true"]',
    # Ô tìm kiếm Asset khi gõ @
    "modal_search_input":        'input#add-menu-input',
    # API tạo Asset
    "api_asset_endpoint_keyword":        "/v1/assets",

    "last_asset": "div[data-tile-id]",

    "asset_title": "div[data-side='bottom'] h4",


}
LOG_MAX_LINES = 1000
LOG_FONT = ("Consolas", 10)
LOG_HEIGHT = 10
LOG_AUTO_SCROLL = True
# Delay
# ==========================================================
SHORT_DELAY = 1
NORMAL_DELAY = 3
LONG_DELAY = 5
POLL_INTERVAL = 2
GENERATE_WAIT_TIME =60

# ==========================================================
# Browser
# ==========================================================

HEADLESS = False

BROWSER_TYPE = "chromium"

# Chrome phải được mở bằng:
# chrome.exe --remote-debugging-port=9222
CHROME_CDP_PORT = 9222
CDP_URL = f"http://127.0.0.1:{CHROME_CDP_PORT}"
# Thời gian chờ nhận Asset từ Google Flow
NETWORK_TIMEOUT = 30.0
DEFAULT_TIMEOUT = 30000
