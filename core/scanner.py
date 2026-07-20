import json
import os

DATABASE_FILE = os.path.join(
    os.path.dirname(__file__),
    "app_database.json"
)

SEARCH_FOLDERS = [
    r"C:\Program Files",
    r"C:\Program Files (x86)",
    os.path.expandvars(r"%LOCALAPPDATA%\Programs"),
    os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"),
    r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
]


def save_database(database):
    with open(DATABASE_FILE, "w", encoding="utf-8") as f:
        json.dump(database, f, indent=4)


def load_database():

    if not os.path.exists(DATABASE_FILE):
        return {}

    with open(DATABASE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def scan_apps():

    print("Scanning installed applications...")

    database = {}

    for folder in SEARCH_FOLDERS:

        if not os.path.exists(folder):
            continue

        for root, dirs, files in os.walk(folder):

            for file in files:

                if file.endswith(".exe") or file.endswith(".lnk"):

                    name = os.path.splitext(file)[0]

                    path = os.path.join(root, file)

                    database[name.lower()] = path

    save_database(database)

    print(f"Found {len(database)} applications.")

    return database


if __name__ == "__main__":
    scan_apps()