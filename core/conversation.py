import time

from core.router import Router
from core.voice import (
    speak,
    listen,
    stop_speaking
)
from core.state import AssistantState


class ConversationManager:

    def __init__(
        self,
        state_manager,
        ui_callback=None,
        voice_enabled=True
    ):

        self.state = state_manager

        self.ui_callback = ui_callback

        self.voice_enabled = voice_enabled

        self.router = Router()

        self.timeout = 30

    # ------------------------------------------

    def set_voice(self, enabled):

        self.voice_enabled = enabled

    # ------------------------------------------

    def set_ui_callback(self, callback):

        self.ui_callback = callback

    # ------------------------------------------

    def say(self, text):

        if self.ui_callback:
            self.ui_callback("JARVIS", text)

        if self.voice_enabled:
            speak(text)

    # ------------------------------------------

    def chat(self, first_command=""):

        self.state.set(
            AssistantState.LISTENING
        )

        if first_command == "":

            self.say(
                "Yes Sir. I'm listening."
            )

            command = listen(
                timeout=8,
                phrase_time_limit=12
            )

        else:

            command = first_command

        last_activity = time.time()

        while True:

            # -----------------------------
            # Timeout
            # -----------------------------

            if command == "":

                if (
                    time.time() - last_activity
                    > self.timeout
                ):

                    self.state.set(
                        AssistantState.SLEEPING
                    )

                    return

                command = listen(
                    timeout=5,
                    phrase_time_limit=12
                )

                continue

            command = command.strip()

            # -----------------------------
            # Stop Speaking
            # -----------------------------

            if command.lower() in [

                "stop",
                "stop speaking",
                "cancel",
                "quiet"

            ]:

                stop_speaking()

                command = ""

                continue

            # -----------------------------
            # User Message
            # -----------------------------

            if self.ui_callback:

                self.ui_callback(
                    "You",
                    command
                )

            self.state.set(
                AssistantState.THINKING
            )

            # -----------------------------
            # Router
            # -----------------------------

            answer = self.router.route(
                command
            )

            self.state.set(
                AssistantState.SPEAKING
            )

            self.say(answer)

            last_activity = time.time()

            self.state.set(
                AssistantState.LISTENING
            )

            command = listen(
                timeout=20,
                phrase_time_limit=12
            )