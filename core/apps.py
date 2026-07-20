import subprocess
import webbrowser
import os


APPS = {

    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "google chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "google": r"C:\Program Files\Google\Chrome\Application\chrome.exe",

    "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",

    "notepad": "notepad.exe",

    "calculator": "calc.exe",
    "calc": "calc.exe",

    "paint": "mspaint.exe",

    "cmd": "cmd.exe",

    "powershell": "powershell.exe",

    "task manager": "taskmgr.exe",

    "explorer": "explorer.exe",

    "vscode": r"C:\Users\Khawar Rafiq\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd",
    "vs code": r"C:\Users\Khawar Rafiq\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd",
}


def open_app(name):

    name = name.lower().strip()

    if name not in APPS:
        return False, f"I couldn't find {name}"

    app = APPS[name]

    try:

        # Launch executables
        if app.endswith(".exe"):

            os.startfile(app)

        # Launch CMD scripts (VS Code)
        elif app.endswith(".cmd"):

            subprocess.Popen(
                app,
                shell=True
            )

        else:

            subprocess.Popen(
                app,
                shell=True
            )

        return True, f"Opening {name}"

    except Exception as e:

        return False, f"Error: {e}"


def open_website(url):

    try:

        if not url.startswith("http"):
            url = "https://" + url

        webbrowser.open(url)

        return True, f"Opening {url}"

    except Exception as e:

        return False, str(e)