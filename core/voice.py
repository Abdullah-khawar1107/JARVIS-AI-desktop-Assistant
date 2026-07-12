import threading
import pyttsx3
import speech_recognition as sr


# Create ONE recognizer
recognizer = sr.Recognizer()

# Create ONE microphone
microphone = sr.Microphone()

# Voice settings
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True


# -----------------------
# TEXT TO SPEECH
# -----------------------

def _speak(text):

    engine = pyttsx3.init()

    engine.setProperty("rate", 180)

    engine.say(text)

    engine.runAndWait()

    engine.stop()


def speak(text):

    thread = threading.Thread(
        target=_speak,
        args=(text,)
    )

    thread.daemon = True

    thread.start()


# -----------------------
# SPEECH TO TEXT
# -----------------------

def listen():

    try:

        with microphone as source:

            print("Listening...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=10
            )

        text = recognizer.recognize_google(audio)

        print("You said:", text)

        return text.lower()

    except Exception as e:

        print("Voice Error:", e)

        return ""