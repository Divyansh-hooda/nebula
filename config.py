import os
APP_NAME = "Nebula"
WINDOW_WIDTH = 1350
WINDOW_HEIGHT = 820
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "database")
DATABASE_FILE = os.path.join(DATABASE_DIR, "nebula.db")
VAULT_DIR = os.path.join(BASE_DIR, "vault")
LOG_DIR = os.path.join(BASE_DIR, "logs")
ICON_DIR = os.path.join(BASE_DIR, "icons")
THEME = "dark"
BACKGROUND = "#1d1d1d"
SIDEBAR = "#272727"
TOPBAR = "#303030"
TEXT = "white"
ACCENT = "#3daee9"
FONT = ("Segoe UI",10)
BIG_FONT = ("Segoe UI",14,"bold")