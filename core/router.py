from core.ai import ask_ai
from core.apps import (
    open_app,
    open_website,
)


class Router:

    def __init__(self):

        self.open_words = [
            "open",
            "launch",
            "start",
            "run"
        ]

        self.websites = {

            "youtube": "https://youtube.com",
            "google": "https://google.com",
            "gmail": "https://mail.google.com",
            "github": "https://github.com",
            "chatgpt": "https://chat.openai.com",
            "facebook": "https://facebook.com",
            "instagram": "https://instagram.com",
            "linkedin": "https://linkedin.com",
            "x": "https://x.com",
            "twitter": "https://x.com",
            "netflix": "https://netflix.com",
            "amazon": "https://amazon.com"

        }

    # -------------------------------------------------

    def clean(self, command):

        command = command.lower().strip()

        wake_words = [

            "jarvis",
            "hey jarvis",
            "hello jarvis",
            "hey"

        ]

        for wake in wake_words:

            command = command.replace(wake, "")

        return command.strip()

    # -------------------------------------------------

    def open_command(self, command):

        for word in self.open_words:

            if command.startswith(word + " "):

                target = command[len(word):].strip()

                # Website first
                if target in self.websites:

                    ok, msg = open_website(
                        self.websites[target]
                    )

                    return msg

                # Installed application
                ok, msg = open_app(target)

                return msg

        return None

    # -------------------------------------------------

    def website_command(self, command):

        prefixes = [

            "go to ",
            "visit "

        ]

        for prefix in prefixes:

            if command.startswith(prefix):

                url = command.replace(prefix, "").strip()

                ok, msg = open_website(url)

                return msg

        return None

    # -------------------------------------------------

    def route(self, command):

        command = self.clean(command)

        if command == "":
            return "Yes Sir."

        # ------------------------
        # OPEN
        # ------------------------

        result = self.open_command(command)

        if result:
            return result

        # ------------------------
        # WEBSITE
        # ------------------------

        result = self.website_command(command)

        if result:
            return result

        # ------------------------
        # AI
        # ------------------------

        return ask_ai(command)