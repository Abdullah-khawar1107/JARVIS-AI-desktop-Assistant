from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton
)

from core.brain import Brain


class JarvisWindow(QWidget):

    update_chat = Signal(str, str)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("JARVIS")
        self.resize(650, 550)

        # Brain
        self.brain = Brain()
        self.brain.set_ui_callback(self.add_message)

        self.voice_enabled = True

        layout = QVBoxLayout()

        self.title = QLabel("JARVIS AI Assistant")

        self.chat_box = QTextEdit()
        self.chat_box.setReadOnly(True)
        self.chat_box.setText("JARVIS: Hello, how can I help you?")

        self.thinking_label = QLabel("")

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type your message...")

        self.send_button = QPushButton("Send")

        self.voice_button = QPushButton("Voice: ON")

        # Signals
        self.send_button.clicked.connect(self.send_message)
        self.input_box.returnPressed.connect(self.send_message)
        self.voice_button.clicked.connect(self.toggle_voice)

        self.update_chat.connect(self.append_chat)

        layout.addWidget(self.title)
        layout.addWidget(self.chat_box)
        layout.addWidget(self.thinking_label)
        layout.addWidget(self.input_box)
        layout.addWidget(self.send_button)
        layout.addWidget(self.voice_button)

        self.setLayout(layout)

        # Start Wake Listener
        self.brain.start()

    # ------------------------------------
    # Add chat safely from another thread
    # ------------------------------------

    def add_message(self, sender, message):
        self.update_chat.emit(sender, message)

    def append_chat(self, sender, message):
        self.chat_box.append(f"{sender}: {message}")

    # ------------------------------------
    # Voice Toggle
    # ------------------------------------

    def toggle_voice(self):

        self.voice_enabled = not self.voice_enabled

        self.brain.set_voice(self.voice_enabled)

        if self.voice_enabled:
            self.voice_button.setText("Voice: ON")
        else:
            self.voice_button.setText("Voice: OFF")

    # ------------------------------------
    # Text Message
    # ------------------------------------

    def send_message(self):

        message = self.input_box.text().strip()

        if message == "":
            return

        self.chat_box.append("You: " + message)

        self.thinking_label.setText("JARVIS is thinking...")

        response = self.brain.ask(message)

        self.thinking_label.setText("")

        self.chat_box.append("JARVIS: " + response)

        self.input_box.clear()

        self.input_box.setFocus()