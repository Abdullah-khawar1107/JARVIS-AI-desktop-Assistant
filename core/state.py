from enum import Enum


class AssistantState(Enum):

    SLEEPING = 1

    LISTENING = 2

    THINKING = 3

    SPEAKING = 4


class StateManager:

    def __init__(self):

        self.state = AssistantState.SLEEPING

    def set(self, state):

        self.state = state

        print(f"[STATE] -> {state.name}")

    def get(self):

        return self.state

    def is_sleeping(self):

        return self.state == AssistantState.SLEEPING

    def is_listening(self):

        return self.state == AssistantState.LISTENING

    def is_thinking(self):

        return self.state == AssistantState.THINKING

    def is_speaking(self):

        return self.state == AssistantState.SPEAKING