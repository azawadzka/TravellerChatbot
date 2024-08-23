from abc import ABC, abstractmethod

from langchain.vectorstores.base import VectorStore


class Retriever(ABC):
    @abstractmethod
    def retrieve(*args, **kwargs) -> str:
        pass


class SimilaritySearchRetriever(Retriever):
    K = 3

    def retrieve(self, vector_store: VectorStore, query: str) -> str:
        return str(vector_store.similarity_search(query, self.K))
