import threading

from core.ai import ask_ai
from core.voice import speak
from core.wake import WakeListener
from core.state import StateManager
from core.conversation import ConversationManager


class Brain:

    def __init__(self):

        # -----------------------------
        # Settings
        # -----------------------------

        self.voice_enabled = True

        self.ui_callback = None

        # -----------------------------
        # State Manager
        # -----------------------------

        self.state = StateManager()

        # -----------------------------
        # Wake Listener
        # -----------------------------

        self.wake = WakeListener()

        # -----------------------------
        # Conversation Manager
        # -----------------------------

        self.conversation = ConversationManager(
            state_manager=self.state,
            voice_enabled=self.voice_enabled
        )

    # ====================================================
    # UI CALLBACK
    # ====================================================

    def set_ui_callback(self, callback):

        self.ui_callback = callback

        self.conversation.set_ui_callback(callback)

    # ====================================================
    # VOICE
    # ====================================================

    def set_voice(self, enabled):

        self.voice_enabled = enabled

        self.conversation.set_voice(enabled)

    # ====================================================
    # TEXT CHAT
    # ====================================================

    def ask(self, message):

        if self.ui_callback:
            self.ui_callback("You", message)

        answer = ask_ai(message)

        if self.ui_callback:
            self.ui_callback("JARVIS", answer)

        if self.voice_enabled:
            speak(answer)

        return answer

    # ====================================================
    # START
    # ====================================================

    def start(self):

        self.wake.start(
            self.on_wake
        )

    # ====================================================
    # WAKE CALLBACK
    # ====================================================

    def on_wake(self, command):

        thread = threading.Thread(
            target=self.run_conversation,
            args=(command,),
            daemon=True
        )

        thread.start()

    # ====================================================
    # CONVERSATION
    # ====================================================

    def run_conversation(self, command):

        try:

            self.conversation.chat(command)

        finally:

            self.wake.resume()