import os

from src.app.client import Client
from src.app.conversation import Conversation
from src.app.data_sources import DataSources
from src.app.destination_retriever import DestinationRetriever
from src.app.retriever import SimilaritySearchRetriever

os.environ["TOKENIZERS_PARALLELISM"] = "false"  # huggingface/tokenizers warning for SimilaritySearchRetriever


client = Client()

destination_retriever = DestinationRetriever(client)

retriever = SimilaritySearchRetriever()

data = DataSources()

conversation = Conversation(
    client=client,
    destination_retriever=destination_retriever,
    retriever=retriever,
    data=data
)


def get_client() -> Client:
    return client


def get_conversation() -> Conversation:
    return conversation
