import threading
from core.voice import listen


class WakeListener:

    def __init__(self):

        self.running = False
        self.callback = None

    def start(self, callback):

        if self.running:
            return

        self.callback = callback
        self.running = True

        thread = threading.Thread(
            target=self._listen_loop,
            daemon=True
        )

        thread.start()

    def stop(self):

        self.running = False

    def _listen_loop(self):

        print("Wake Listener Started")

        while self.running:

            text = listen()

            if not text:
                continue

            wake_words = [
                "hey jarvis",
                "jarvis",
                "hello jarvis",
                "hey jar"
            ]

            for word in wake_words:

                if word in text:

                    print("Wake Word Detected")

                    command = text.replace(word, "").strip()

                    self.stop()

                    if self.callback:
                        self.callback(command)

                    return