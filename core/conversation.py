import time

from core.ai import ask_ai
from core.voice import speak, listen, stop_speaking
from core.state import AssistantState
from core.apps import open_app


class ConversationManager:

    def __init__(self, state_manager, ui_callback=None, voice_enabled=True):

        self.state = state_manager
        self.ui_callback = ui_callback
        self.voice_enabled = voice_enabled

        self.timeout = 30

    def set_voice(self, enabled):
        self.voice_enabled = enabled

    def set_ui_callback(self, callback):
        self.ui_callback = callback

    def chat(self, first_command=""):

        self.state.set(AssistantState.LISTENING)

        if first_command == "":

            if self.ui_callback:
                self.ui_callback("JARVIS", "Yes? I'm listening.")

            if self.voice_enabled:
                speak("Yes? I'm listening.")

            command = listen(timeout=8, phrase_time_limit=12)

        else:
            command = first_command

        last_activity = time.time()

        while True:

            if command == "":

                if time.time() - last_activity > self.timeout:

                    self.state.set(AssistantState.SLEEPING)
                    return

                command = listen(
                    timeout=5,
                    phrase_time_limit=12
                )

                continue

            command = command.lower().strip()

            # -------------------------
            # Stop Speaking
            # -------------------------

            if command in [
                "stop",
                "stop speaking",
                "cancel",
                "quiet"
            ]:

                stop_speaking()
                command = ""
                continue

            # -------------------------
            # OPEN APPLICATION
            # -------------------------

            if command.startswith("open "):

                app = command.replace("open ", "").strip()

                ok, answer = open_app(app)

                if self.ui_callback:
                    self.ui_callback("You", command)
                    self.ui_callback("JARVIS", answer)

                if self.voice_enabled:
                    speak(answer)

                last_activity = time.time()

                command = listen(
                    timeout=20,
                    phrase_time_limit=12
                )

                continue

            # -------------------------
            # AI
            # -------------------------

            if self.ui_callback:
                self.ui_callback("You", command)

            self.state.set(AssistantState.THINKING)

            answer = ask_ai(command)

            if self.ui_callback:
                self.ui_callback("JARVIS", answer)

            self.state.set(AssistantState.SPEAKING)

            if self.voice_enabled:
                speak(answer)

            last_activity = time.time()

            self.state.set(AssistantState.LISTENING)

            command = listen(
                timeout=20,
                phrase_time_limit=12
            )