from pathlib import Path


APP = "main:app"
HOST = "127.0.0.1"
PORT = 8000
WORKERS = 1

DB_FILE = "comp-server.db"
DB_CONN_STR = f"sqlite:///{DB_FILE}"
DB_CONN_ARGS = {"check_same_thread": False}

CWD = Path.cwd()
DIR_ENUMS_ABS_PATH = Path.absolute(CWD / "enums")
DIR_DB_ABS_PATH = Path.absolute(CWD / "database")
DIR_ROUTER_ABS_PATH = Path.absolute(CWD / "routers")