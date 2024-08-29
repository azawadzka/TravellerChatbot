import tiktoken
from openai import OpenAI

from src.app.helpers import get_secret


class Client:
    TOKENS_LIMIT = 4096
    MAX_RESPONSE_TOKENS = 800
    MODEL = "gpt-3.5-turbo"

    def __init__(self):
        self.client = OpenAI(
            api_key=get_secret("OPENAI_API_KEY")
        )

    def chat(self, conversation) -> str:
        response = self.client.chat.completions.create(
            model=Client.MODEL,
            messages=conversation,
            temperature=0.7,
            max_tokens=self.MAX_RESPONSE_TOKENS,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        return response.choices[0].message.content

    def get_tokens_count(self, messages) -> int:
        try:
            encoding = tiktoken.encoding_for_model(self.MODEL)
        except KeyError:
            print("Warning: model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")
        # for gpt-3.5-turbo-0613
        tokens_per_message = 3
        tokens_per_name = 1
        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
        return num_tokens


if __name__ == '__main__':
    client = Client()
    conversation = [{"role": "system", "content": "You are an AI assistant that helps people answer questions travel destinations in Portugal"}]  # noqa
    conversation.append({"role": "user", "content": "What can I do in Madeira?"})
    response = client.chat(conversation)
    print(response)
