import json
import os
import subprocess
import webbrowser
from pathlib import Path
from difflib import get_close_matches


ROOT = Path(__file__).parent

DATABASE = ROOT / "app_database.json"


class AppManager:

    def __init__(self):

        self.apps = {}

        self.aliases = {

            "google": "chrome",
            "browser": "chrome",
            "google chrome": "chrome",

            "vs code": "code",
            "visual studio": "code",
            "visual studio code": "code",
            "vscode": "code",

            "cmd": "command prompt",
            "terminal": "command prompt",

            "paint": "mspaint",

            "calc": "calculator",

            "explorer": "file explorer",

            "task manager": "taskmgr",

            "word": "microsoft word",
            "excel": "microsoft excel",
            "ppt": "powerpoint",
            "power point": "powerpoint",

        }

        self.load_database()

    # -----------------------------------

    def load_database(self):

        self.apps.clear()

        if not DATABASE.exists():

            print("app_database.json not found")

            return

        try:

            with open(DATABASE, "r", encoding="utf-8") as f:

                self.apps = json.load(f)

        except Exception as e:

            print(e)

            self.apps = {}

    # -----------------------------------

    def reload(self):

        self.load_database()

    # -----------------------------------

    def exists(self, app):

        return app.lower() in self.apps

    # -----------------------------------

    def normalize(self, name):

        name = name.lower().strip()

        if name in self.aliases:

            name = self.aliases[name]

        return name

    # -----------------------------------

    def fuzzy(self, name):

        if name in self.apps:

            return name

        matches = get_close_matches(

            name,

            self.apps.keys(),

            n=1,

            cutoff=0.55

        )

        if matches:

            return matches[0]

        return None

    # -----------------------------------

    def get_path(self, name):

        name = self.normalize(name)

        if name in self.apps:

            return self.apps[name]

        match = self.fuzzy(name)

        if match:

            return self.apps[match]

        return None

    # -----------------------------------

    def open_path(self, path):

        try:

            path = os.path.expandvars(path)

            if path.lower().endswith(".url"):

                webbrowser.open(path)

                return True

            if path.lower().startswith("http"):

                webbrowser.open(path)

                return True

            if path.lower().endswith(".cmd"):

                subprocess.Popen(

                    path,

                    shell=True

                )

                return True

            if path.lower().endswith(".bat"):

                subprocess.Popen(

                    path,

                    shell=True

                )

                return True

            os.startfile(path)

            return True

        except Exception as e:

            print(e)

            return False
        
    # -----------------------------------

    def open(self, app_name):
        app_name = app_name.lower().strip()

        # -------------------------
        # Windows Built-in Apps
        # -------------------------

        if app_name in ["calculator", "calc"]:
            try:
                subprocess.Popen("calc.exe", shell=True)
                return True, "Opening Calculator"
            except Exception as e:
                return False, str(e)

        if app_name in ["notepad"]:
            try:
                subprocess.Popen("notepad.exe", shell=True)
                return True, "Opening Notepad"
            except Exception as e:
                return False, str(e)

        if app_name in ["paint", "mspaint"]:
            try:
                subprocess.Popen("mspaint.exe", shell=True)
                return True, "Opening Paint"
            except Exception as e:
                return False, str(e)

        if app_name in ["command prompt", "cmd"]:
            try:
                subprocess.Popen("cmd.exe", shell=True)
                return True, "Opening Command Prompt"
            except Exception as e:
                return False, str(e)

        # -------------------------
        # Installed Apps
        # -------------------------

        path = self.get_path(app_name)

        if not path:
            return False, f"I couldn't find {app_name}"

        ok = self.open_path(path)

        if ok:
            return True, f"Opening {app_name}"

        return False, f"Failed to open {app_name}"

    # -----------------------------------

    def list_apps(self):

        return sorted(self.apps.keys())

    # -----------------------------------

    def search(self, keyword):

        keyword = keyword.lower()

        results = []

        for app in self.apps:

            if keyword in app:

                results.append(app)

        return results

    # -----------------------------------

    def count(self):

        return len(self.apps)


# ======================================================
# GLOBAL MANAGER
# ======================================================

_manager = AppManager()


# ======================================================
# PUBLIC FUNCTIONS
# ======================================================

def reload_apps():
    _manager.reload()


def total_apps():
    return _manager.count()


def list_apps():
    return _manager.list_apps()


def search_apps(keyword):
    return _manager.search(keyword)


def open_app(app_name):
    return _manager.open(app_name)


def open_folder(folder):

    try:

        os.startfile(folder)

        return True, f"Opening folder"

    except Exception as e:

        return False, str(e)


def open_file(file_path):

    try:

        os.startfile(file_path)

        return True, "Opening file"

    except Exception as e:

        return False, str(e)


def open_website(url):

    try:

        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url

        webbrowser.open(url)

        return True, f"Opening {url}"

    except Exception as e:

        return False, str(e)


# ======================================================
# TEST
# ======================================================

if __name__ == "__main__":

    print("-" * 50)

    print("JARVIS APP MANAGER")

    print("-" * 50)

    print("Installed Apps:", total_apps())

    while True:

        app = input("\nOpen App > ").strip()

        if app.lower() == "exit":
            break

        ok, msg = open_app(app)

        print(msg)
