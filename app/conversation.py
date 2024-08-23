from app.client import Client
from app.data_sources import DataSources
from app.destination_retriever import DestinationRetriever
from app.retriever import Retriever

prompt = """
You are an AI assistant that helps people answer questions travel destinations in Portugal based on information given in the context.
Instructions:
- Only answer questions related to traveling to Portugal.
- Only use information given in the context.
- If you're unsure of an answer, you can say "I don't know" or "I'm not sure" and ask if you can help this with information about traveling to Portugal.
- If the context is "unknown", ask the user if they would like to ask about any specific place.
- If the context is "not in database", tell the user that you don't have information about this place.

Context:
{context}
"""


class Conversation:
    SYSTEM_MESSAGES = [{"role": "system", "content": prompt}]

    def __init__(
            self,
            client: Client,
            destination_retriever: DestinationRetriever,
            retriever: Retriever,
            data: DataSources
    ):
        self.client = client
        self.data = data
        self.destination_retriever = destination_retriever
        self.retriever = retriever
        self.messages = self.SYSTEM_MESSAGES[:]
        self.current_destination = None

    def ask(self, question: str) -> str:
        self.messages.append({"role": "user", "content": question})
        self._update_product()
        self._update_context()
        self._remove_overflowing_msgs()
        response = self.client.chat(self.messages)
        self.messages.append({"role": "assistant", "content": response})
        return response

    def _update_product(self) -> None:
        destination = self.destination_retriever.retrieve(self.messages)
        if destination != DestinationRetriever.UNKNOWN_KWD:
            self.current_destination = destination

    def _update_context(self) -> None:
        if not self.current_destination:
            data = "unknown"
        elif self.current_destination not in self.data:
            data = "not in database"
        else:
            data = self.retriever.retrieve(
                vector_store=self.data[self.current_destination],
                query=self.messages[-1]["content"]
            )
        self.messages[0]["content"] = prompt.format(context=data)

    def _remove_overflowing_msgs(self) -> None:
        while self.client.get_tokens_count(self.messages) + self.client.MAX_RESPONSE_TOKENS >= self.client.TOKENS_LIMIT:
            del self.messages[len(self.SYSTEM_MESSAGES)]  # the message after system messages
