import os

from app.client import Client
from app.conversation import Conversation
from app.data_sources import DataSources
from app.destination_retriever import DestinationRetriever
from app.retriever import SimilaritySearchRetriever

os.environ["TOKENIZERS_PARALLELISM"] = "false"  # huggingface/tokenizers warning for SimilaritySearchRetriever


client = Client()


def get_client() -> Client:
    return client


destination_retriever = DestinationRetriever(client)

retriever = SimilaritySearchRetriever()

data = DataSources()

conversation = Conversation(
    client=client,
    destination_retriever=destination_retriever,
    retriever=retriever,
    data=data
)


def get_conversation() -> Conversation:
    return conversation
