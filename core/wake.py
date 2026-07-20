import threading
from core.voice import listen


class WakeListener:

    def __init__(self):

        self.callback = None
        self.active = True
        self.thread = None

    # --------------------------------
    # Start Once
    # --------------------------------

    def start(self, callback):

        self.callback = callback

        if self.thread is not None:
            return

        self.thread = threading.Thread(
            target=self._loop,
            daemon=True
        )

        self.thread.start()

        print("Wake Listener Started")

    # --------------------------------
    # Pause
    # --------------------------------

    def pause(self):

        self.active = False

    # --------------------------------
    # Resume
    # --------------------------------

    def resume(self):

        self.active = True

    # --------------------------------
    # Main Loop
    # --------------------------------

    def _loop(self):

        wake_words = [
            "jarvis",
            "hey jarvis",
            "hello jarvis",
            "hey jar"
        ]

        while True:

            if not self.active:
                continue

            text = listen(
                timeout=5,
                phrase_time_limit=8
            )

            if text == "":
                continue

            for word in wake_words:

                if word in text:

                    print("Wake Word Detected")

                    command = text.replace(word, "").strip()

                    self.pause()

                    if self.callback:
                        self.callback(command)

                    break