import threading

from core.ai import ask_ai
from core.voice import speak
from core.wake import WakeListener
from core.state import StateManager
from core.conversation import ConversationManager
from core.apps import open_app


class Brain:

    def __init__(self):

        self.voice_enabled = True

        self.ui_callback = None

        self.state = StateManager()

        self.wake = WakeListener()

        self.conversation = ConversationManager(
            self.state,
            voice_enabled=self.voice_enabled
        )

    # -----------------------------
    # UI
    # -----------------------------

    def set_ui_callback(self, callback):

        self.ui_callback = callback

        self.conversation.set_ui_callback(callback)

    # -----------------------------
    # Voice
    # -----------------------------

    def set_voice(self, enabled):

        self.voice_enabled = enabled

        self.conversation.set_voice(enabled)

    # -----------------------------
    # Text Chat
    # -----------------------------

    def ask(self, message):

        message = message.lower()

        if message.startswith("open "):

            app = message.replace("open ", "").strip()

            ok, reply = open_app(app)

            if self.voice_enabled:
                speak(reply)

            return reply

        answer = ask_ai(message)

        if self.voice_enabled:
            speak(answer)

        return answer

    # -----------------------------
    # Start
    # -----------------------------

    def start(self):

        self.wake.start(self.on_wake)

    # -----------------------------
    # Wake Callback
    # -----------------------------

    def on_wake(self, command):

        thread = threading.Thread(
            target=self._conversation,
            args=(command,),
            daemon=True
        )

        thread.start()

    # -----------------------------
    # Conversation
    # -----------------------------

    def _conversation(self, command):

        if command.lower().startswith("open "):

            app = command.replace("open ", "").strip()

            ok, reply = open_app(app)

            if self.ui_callback:
                self.ui_callback("JARVIS", reply)

            if self.voice_enabled:
                speak(reply)

            self.wake.resume()

            return

        self.conversation.chat(command)

        self.wake.resume()