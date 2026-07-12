from core.voice import speak, listen

while True:

    command = listen()

    if command == "":

        continue

    if command == "exit":

        speak("Goodbye")

        break

    print(command)

    speak("You said " + command)