from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory

from app.deps import get_conversation


if __name__ == '__main__':
    session = PromptSession(history=FileHistory(".cli-history"))

    conversation = get_conversation()
    print("S: Hello, I'm a travel assistant. Ask me about your dream destination.")
    while True:
        user_input = session.prompt("Q: ")
        response = conversation.ask(user_input)
        print("U: " + response)
