import os
from pathlib import Path
from typing import Optional

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.base import VectorStore
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings


class DataSources:
    data_path = Path("./data")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2", cache_folder="models")

    def __init__(self, path: Optional[str] = None):
        self.data = self._load_data(path or self.data_path)
        self.vector_stores = {key: self._make_vectorstore(documents) for key, documents in self.data.items()}

    def __getitem__(self, item) -> VectorStore:
        return self.vector_stores[item]

    def __contains__(self, item):
        return item in self.vector_stores

    @staticmethod
    def _load_data(dir_path):
        filepaths = [dir_path / fp for fp in os.listdir(dir_path)]
        filtered_paths = [fp for fp in filepaths if not fp.name.startswith((".", "_"))]
        data = {fp.stem.lower(): DataSources._load_pdf(fp) for fp in filtered_paths}
        return data

    @staticmethod
    def _load_pdf(path: Path):
        loader = PyPDFLoader(path)
        data = loader.load_and_split()
        return data

    @staticmethod
    def _make_vectorstore(documents: list[Document]):
        splits = DataSources.text_splitter.split_documents(documents)
        return Chroma.from_documents(splits, DataSources.embedding_function)


if __name__ == '__main__':
    ds = DataSources()
    for file, content in ds.data.items():
        print(file)
        for page in content:
            print(page)
