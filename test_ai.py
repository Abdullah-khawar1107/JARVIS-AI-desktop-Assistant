from core.ai import ask_ai

while True:

    question = input("You: ")

    if question.lower() == "exit":
        break

    answer = ask_ai(question)

    print("JARVIS:", answer)