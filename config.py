import os
APP_NAME = "Nebula"
WINDOW_WIDTH = 1350
WINDOW_HEIGHT = 820
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "database")
DATABASE_FILE = os.path.join(DATABASE_DIR, "nebula.db")
VAULT_DIR = os.path.join(BASE_DIR, "vault")