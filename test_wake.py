from core.wake import WakeListener
from core.voice import speak

listener = WakeListener()


def wake():

    print("JARVIS is awake!")

    speak("Yes, I am listening.")


listener.start(wake)

input("Press ENTER to quit...")