import json
from typing import List

from app.client import Client

prompt = """
Return JSON having one field "destination" containing name of the last travel destination that the user asked about in the context. If you don't know, fill the field with the word "unknown".
Context: {context}
"""


class DestinationRetriever:
    N_MESSAGES = 3
    UNKNOWN_KWD = "unknown"

    def __init__(self, client: Client):
        self.client = client

    def retrieve(self, messages: List[dict]) -> str:
        context = self._format_context(self._select_messages(messages))
        request = [{"role": "system", "content": prompt.format(context=context)}]
        json_str_response = self.client.chat(request)
        return self._parse_response(json_str_response)

    @staticmethod
    def _select_messages(messages: List[dict]) -> List[dict]:
        """
        Select n=ProductRetriever.N_MESSAGES latest messages that are either user or assistant, not system.
        This should help to build sufficient context for retrieval.
        """
        return [msg for msg in messages if msg["role"] in ["user", "assistant"]][-DestinationRetriever.N_MESSAGES:]

    @staticmethod
    def _format_context(messages: List[dict]) -> str:
        return "\n".join(f"{msg['role']}: {msg['content']}" for msg in messages)

    @staticmethod
    def _parse_response(json_str_response: str) -> str:
        try:
            return json.loads(json_str_response)["destination"].lower()
        except Exception:
            return "unknown"


if __name__ == '__main__':
    client = Client()
    dr = DestinationRetriever(client)
    destination = dr.retrieve([{"role": "user", "content": "What can I do in Madeira?"}])
    print(destination)
