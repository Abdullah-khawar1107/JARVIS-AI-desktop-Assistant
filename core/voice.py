import asyncio
import os
import tempfile
import threading

import edge_tts
import pygame
import speech_recognition as sr

# ==========================================
# Speech Recognition
# ==========================================

recognizer = sr.Recognizer()
microphone = sr.Microphone()

recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True

# ==========================================
# Audio Player
# ==========================================

pygame.mixer.init()

_lock = threading.Lock()
_stop_event = threading.Event()

_current_thread = None
_current_file = None

is_speaking = False

VOICE = "en-US-GuyNeural"

# ==========================================
# Edge TTS
# ==========================================


async def _generate(text, filename):
    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE
    )

    await communicate.save(filename)


# ==========================================
# Player
# ==========================================


def _player(text):

    global is_speaking
    global _current_file

    with _lock:

        is_speaking = True
        _stop_event.clear()

        filename = tempfile.mktemp(".mp3")
        _current_file = filename

        try:

            asyncio.run(
                _generate(text, filename)
            )

            if _stop_event.is_set():
                return

            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():

                if _stop_event.is_set():

                    pygame.mixer.music.stop()
                    break

                pygame.time.wait(50)

        except Exception as e:

            print("Speak Error:", e)

        finally:

            is_speaking = False

            try:
                pygame.mixer.music.unload()
            except:
                pass

            if os.path.exists(filename):

                try:
                    os.remove(filename)
                except:
                    pass


# ==========================================
# Public API
# ==========================================


def speak(text):

    global _current_thread

    stop_speaking()

    _current_thread = threading.Thread(
        target=_player,
        args=(text,),
        daemon=True
    )

    _current_thread.start()


def stop_speaking():

    global is_speaking

    _stop_event.set()

    try:
        pygame.mixer.music.stop()
    except:
        pass

    is_speaking = False


def speaking():

    return is_speaking


# ==========================================
# Speech To Text
# ==========================================


def listen(timeout=10, phrase_time_limit=10):

    try:

        with microphone as source:

            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit
            )

        text = recognizer.recognize_google(audio)

        print("You said:", text)

        return text.lower()

    except sr.WaitTimeoutError:
        return ""

    except sr.UnknownValueError:
        return ""

    except Exception as e:
        print("Voice Error:", e)
        return ""