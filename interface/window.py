from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
)

from core.brain import Brain
from core.voice import stop_speaking


class JarvisWindow(QWidget):

    update_chat = Signal(str, str)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("JARVIS AI Assistant")
        self.resize(700, 600)

        self.brain = Brain()
        self.brain.set_ui_callback(self.add_message)

        self.voice_enabled = True

        layout = QVBoxLayout()

        # ----------------------------
        # Title
        # ----------------------------

        self.title = QLabel("🤖 JARVIS AI Assistant")

        # ----------------------------
        # Chat
        # ----------------------------

        self.chat_box = QTextEdit()
        self.chat_box.setReadOnly(True)
        self.chat_box.append("JARVIS: Hello Sir. How can I help you today?")

        # ----------------------------
        # Status
        # ----------------------------

        self.status = QLabel("Status : Sleeping")

        # ----------------------------
        # Input
        # ----------------------------

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Ask JARVIS anything...")

        # ----------------------------
        # Buttons
        # ----------------------------

        self.send_button = QPushButton("Send")

        self.voice_button = QPushButton("Voice : ON")

        self.stop_button = QPushButton("Stop Speaking")

        # ----------------------------
        # Signals
        # ----------------------------

        self.send_button.clicked.connect(self.send_message)

        self.input_box.returnPressed.connect(self.send_message)

        self.voice_button.clicked.connect(self.toggle_voice)

        self.stop_button.clicked.connect(stop_speaking)

        self.update_chat.connect(self.append_chat)

        # ----------------------------
        # Layout
        # ----------------------------

        layout.addWidget(self.title)

        layout.addWidget(self.chat_box)

        layout.addWidget(self.status)

        layout.addWidget(self.input_box)

        layout.addWidget(self.send_button)

        layout.addWidget(self.voice_button)

        layout.addWidget(self.stop_button)

        self.setLayout(layout)

        # ----------------------------
        # Start JARVIS
        # ----------------------------

        self.brain.start()

    # ===================================
    # Thread Safe Chat
    # ===================================

    def add_message(self, sender, message):

        self.update_chat.emit(sender, message)

    def append_chat(self, sender, message):

        self.chat_box.append(f"{sender}: {message}")

        self.chat_box.verticalScrollBar().setValue(
            self.chat_box.verticalScrollBar().maximum()
        )

    # ===================================
    # Voice Toggle
    # ===================================

    def toggle_voice(self):

        self.voice_enabled = not self.voice_enabled

        self.brain.set_voice(self.voice_enabled)

        if self.voice_enabled:

            self.voice_button.setText("Voice : ON")

        else:

            self.voice_button.setText("Voice : OFF")

    # ===================================
    # Text Chat
    # ===================================

    def send_message(self):

        message = self.input_box.text().strip()

        if message == "":
            return

        self.chat_box.append(f"You: {message}")

        self.status.setText("Status : Thinking...")

        response = self.brain.ask(message)

        self.chat_box.append(f"JARVIS: {response}")

        self.status.setText("Status : Ready")

        self.input_box.clear()

        self.input_box.setFocus()