from core.ai import ask_ai
from core.voice import speak, listen
from core.wake import WakeListener

import threading


class Brain:

    def __init__(self):

        self.voice_enabled = True

        self.ui_callback = None

        self.wake = WakeListener()

    def set_ui_callback(self, callback):

        self.ui_callback = callback

    def set_voice(self, enabled):

        self.voice_enabled = enabled

    def ask(self, message):

        answer = ask_ai(message)

        if self.voice_enabled:
            speak(answer)

        return answer

    def start(self):

        self.wake.start(self.on_wake)

    def on_wake(self, command):

        thread = threading.Thread(
            target=self.process_command,
            args=(command,),
            daemon=True
        )

        thread.start()

    def process_command(self, command):

        if command == "":

            msg = "Yes? I am listening."

            if self.ui_callback:
                self.ui_callback("JARVIS", msg)

            if self.voice_enabled:
                speak(msg)

            command = listen()

        if command == "":

            self.wake.start(self.on_wake)

            return

        print("Command:", command)

        if self.ui_callback:
            self.ui_callback("You", command)

        answer = ask_ai(command)

        if self.ui_callback:
            self.ui_callback("JARVIS", answer)

        if self.voice_enabled:
            speak(answer)

        self.wake.start(self.on_wake)