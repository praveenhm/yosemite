from yosemite.transformers.text import Chunker
from yosemite.transformers.transform import CrossEncoder
from sentence_transformers import SentenceTransformer
from typing import List, Tuple, Optional, Dict, Union
import concurrent.futures
import os
import uuid
from annoy import AnnoyIndex
from whoosh.query import Or, Term
from whoosh.qparser import QueryParser
from whoosh import index as whoosh_index
from whoosh.analysis import StandardAnalyzer, FancyAnalyzer, LanguageAnalyzer, KeywordAnalyzer
from whoosh.fields import Schema, TEXT, ID, KEYWORD, STORED
from whoosh.qparser import QueryParser, QueryParserError, MultifieldParser
import pandas as pd
from PyPDF2 import PdfReader
from ebooklib import epub
import torch

class Database:
    """
    A Unified & Local Database with no backend services required. Built using Whoosh & Annoy. Combines the power of Whoosh for text search and Annoy for vector search, to deliver incredibly easy to use and powerful search capabilities.

    ```python
    from yosemite.ml.database import YosemiteDatabase
    ```

    Attributes:
        dimension (int): The dimension of the vectors.
        model_name (str): The name of the SentenceTransformer model to be used.
        schema (Schema): The schema to be used for the Whoosh index.
        index_dir (str): The directory where the Whoosh index is stored.
        analyzer (str): The type of analyzer to be used for the Whoosh index.

    Args:
        dimension (int, optional): The dimension of the vectors. Defaults to None.
        model_name (str, optional): The name of the SentenceTransformer model to be used. Defaults to "all-MiniLM-L6-v2".
        schema (Schema, optional): The schema to be used for the Whoosh index. Defaults to None.
        analyzer (str, optional): The type of analyzer to be used for the Whoosh index. Defaults to "standard".

    Methods:
        load: Load an existing Whoosh index.
        create: Create a new Whoosh index.
        load_dataset: Load a dataset into the Whoosh index.
        load_docs: Load documents from a directory into the Whoosh index.
        add: Add documents to the Whoosh index.
        search: Search the Whoosh index.
        search_and_rank: Search and rank the Whoosh index.
    """
    def __init__(self, dimension: Optional[int] = None, bert_model: Optional[str] = None, 
                 schema: Optional[Schema] = None, whoosh_analyzer: Optional[str] = "standard"):
        self.index = None
        self.dimension = dimension
        self.model_name = bert_model
        self.ix = None
        self.schema = schema
        self.analyzer = whoosh_analyzer

        if self.schema is None:
            if self.analyzer == "standard":
                self.schema = Schema(id=ID(stored=True), content=TEXT(analyzer=StandardAnalyzer(), stored=True), 
                                     chunks=TEXT(stored=True), vectors=STORED)

        self.index_dir = None

        if self.model_name is None:
            self.model_name = "paraphrase-MiniLM-L6-v2" 
            self.model = SentenceTransformer(self.model_name)
            self.dimension = self.model.get_sentence_embedding_dimension()
        else:
            self.model = SentenceTransformer(self.model_name)
            if self.dimension is None:
                self.dimension = self.model.get_sentence_embedding_dimension()

    def load(self, dir: str):
        """
        A method to load an existing Whoosh index.

        Example:
            ```python
            db = YosemiteDatabase()
            db.load("./databases/db")
            ```

        Args:
            dir (str): The directory where the Whoosh index is stored.
        """
        self.index_dir = dir
        if not os.path.exists(self.index_dir):
            raise FileNotFoundError(f"Index directory {self.index_dir} does not exist.")
        if not whoosh_index.exists_in(self.index_dir):
            raise FileNotFoundError(f"Index does not exist in directory {self.index_dir}.")
        self.ix = whoosh_index.open_dir(self.index_dir)

    def create(self, dir: Optional[str] = None):
        """
        A method to create a new Whoosh index.

        Example:
            ```python
            db = YosemiteDatabase()
            db.create()
            ```

        Args:
            dir (str, optional): The directory where the Whoosh index will be stored. Defaults to None.
        """
        if self.schema is None:
            if self.analyzer == "standard":
                self.schema = Schema(id=ID(stored=True), content=TEXT(analyzer=StandardAnalyzer(), stored=True), 
                                     chunks=TEXT(stored=True), vectors=STORED)
            elif self.analyzer == "fancy":
                self.schema = Schema(id=ID(stored=True), content=TEXT(analyzer=FancyAnalyzer(), stored=True), 
                                     chunks=TEXT(stored=True), vectors=STORED)
            elif self.analyzer == "language":
                self.schema = Schema(id=ID(stored=True), content=TEXT(analyzer=LanguageAnalyzer(), stored=True), 
                                     chunks=TEXT(stored=True), vectors=STORED)
            elif self.analyzer == "keyword":
                self.schema = Schema(id=ID(stored=True), content=KEYWORD(analyzer=KeywordAnalyzer(), stored=True), 
                                     chunks=TEXT(stored=True), vectors=STORED)

        if dir is None:
            self.index_dir = "./databases/db"
        else:
            self.index_dir = dir
        os.makedirs(self.index_dir, exist_ok=True)
        self.ix = whoosh_index.create_in(self.index_dir, self.schema)

    def load_dataset(self, path: str, id_column: str, content_column: str):
        """
        A method to load a CSV dataset into the Whoosh index.

        Example:
            ```python
            db = YosemiteDatabase()
            db.create()
            db.load_dataset("data.csv", "id", "content")
            ```

        Args:
            path (str): The path to the CSV dataset.
            id_column (str): The name of the column containing the document IDs.
            content_column (str): The name of the column containing the document content.
        """
        if not self.ix:
            self.create()
        df = pd.read_csv(path)
        writer = self.ix.writer()
        chunker = Chunker()
        embedder = SentenceTransformer(self.model_name)
        for _, row in df.iterrows():
            doc_id = str(row[id_column])
            doc_content = row[content_column]
            chunks = chunker.chunk(doc_content)
            vectors = [embedder.embed([chunk])[0][1] for chunk in chunks]
            writer.add_document(id=doc_id, content=doc_content, chunks="\n".join(chunks), vectors=vectors)
        writer.commit()

    def load_docs(self, dir: str):
        """
        A very powerful method to load documents from a directory into the Whoosh index. Supports .txt, .pdf, and .epub files.

        Example:
            ```python
            db = YosemiteDatabase()
            db.create()
            db.load_docs("documents")
            ```

        Args:
            dir (str): The directory containing the documents.
        """
        if not self.ix:
            self.create()
        if not os.path.exists(dir):
            raise FileNotFoundError(f"Directory {dir} does not exist.")

        writer = self.ix.writer()
        chunker = Chunker()

        file_paths = [os.path.join(dir, file_path) for file_path in os.listdir(dir)]

        for file_path in file_paths:
            try:
                content = self._read_file(file_path)
                if content:
                    doc_id = str(uuid.uuid4())
                    chunks = chunker.chunk(content)
                    embeddings = self.compute_embeddings(chunks)
                    writer.add_document(id=doc_id, content=content, chunks="\n".join(chunks), vectors=embeddings)
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

        writer.commit()

    def compute_embeddings(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """
        Computes sentence embeddings for the given texts using the specified model.

        Args:
            texts (List[str]): The list of texts to compute embeddings for.
            batch_size (int): The batch size to use for encoding.

        Returns:
            List[List[float]]: The computed sentence embeddings.
        """
        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            batch_embeddings = self.model.encode(batch_texts, convert_to_numpy=True)
            embeddings.extend(batch_embeddings)
        return embeddings

    def _read_file(self, file_path: str) -> str:
        if file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
        elif file_path.endswith(".pdf"):
            with open(file_path, "rb") as file:
                reader = PdfReader(file)
                content = " ".join(page.extract_text() for page in reader.pages)
        elif file_path.endswith(".epub"):
            book = epub.read_epub(file_path)
            content = " ".join(item.get_content().decode("utf-8") for item in book.get_items_of_type(9))
        else:
            content = ""
        return content

    def add(self, documents: List[Dict[str, str]], shared_id: Optional[bool] = False):
        """
        A method to add documents to the Whoosh index.

        Example:
            ```python
            db = YosemiteDatabase()
            db.create()
            documents = [
                {"content": "This is a test document."},
                {"content": "This is another test document."}
            ]
            db.add(documents)
            ```

        Args:
            documents (List[Dict[str, str]]): A list of dictionaries containing the document content.
            shared_id (Optional[bool], optional): Whether to use a shared ID for all documents. Defaults to False.
        """
        if not self.ix:
            self.create()
        writer = self.ix.writer()
        chunker = Chunker()
        embedder = SentenceTransformer(self.model_name)
        for doc in documents:
            if shared_id:
                doc_id = "shared"
            else:
                doc_id = doc.get("id", str(uuid.uuid4()))
            doc_content = doc["content"]
            chunks = chunker.chunk(doc_content)
            vectors = [embedder.embed([chunk])[0][1] for chunk in chunks]
            writer.add_document(id=doc_id, content=doc_content, chunks="\n".join(chunks), vectors=vectors)
        writer.commit()

    def search(self, query: str, fields: Optional[List[str]] = None, k: int = 5, m: int = 3) -> List[Dict[str, Union[str, float]]]:
        if not self.ix:
            raise ValueError("Index has not been built or loaded.")

        with self.ix.searcher() as searcher:
            if fields is None:
                parser = QueryParser("content", schema=self.schema)
            else:
                parser = MultifieldParser(fields, schema=self.schema)
            try:
                q = parser.parse(query)
                results = searcher.search(q, limit=k)
                doc_ids = [hit["id"] for hit in results]
                doc_chunks = [hit["chunks"].split("\n") for hit in results]
                doc_vectors = [hit["vectors"] for hit in results]

                chunk_info = []
                for doc_id, chunks, vectors in zip(doc_ids, doc_chunks, doc_vectors):
                    for chunk, vector in zip(chunks, vectors):
                        chunk_info.append((doc_id, chunk, vector))

                if not self.dimension:
                    self.dimension = len(chunk_info[0][2])

                index = AnnoyIndex(self.dimension, 'angular')
                for i, (_, _, vector) in enumerate(chunk_info):
                    index.add_item(i, vector)

                index.build(10)
                query_vector = self.model.encode([query])[0]
                vector_results = index.get_nns_by_vector(query_vector, k * m, include_distances=True)

                chunk_results = [(chunk_info[idx][0], chunk_info[idx][1]) for idx in vector_results[0]]

                cross_encoder = CrossEncoder()
                ranked_results = cross_encoder.rank(query, [chunk for _, chunk in chunk_results])

                formatted_results = []
                for (doc_id, chunk), score in zip(chunk_results, ranked_results):
                    formatted_results.append({
                        "document_id": doc_id,
                        "chunk": chunk,
                        "relevance_score": score
                    })

                return formatted_results

            except QueryParserError as e:
                print(f"QueryParserError: {e}")
                return []
                
    def search_and_rank(self, query: str, k: int = 5, m: int = 3) -> List[Tuple[str, str, float]]:
        if not self.ix:
            raise ValueError("Index has not been built or loaded.")

        with self.ix.searcher() as searcher:
            qp = QueryParser("content", schema=self.schema)
            q = qp.parse(query)
            keywords = q.all_terms()

        with self.ix.searcher() as searcher:
            q = Or([Term("content", keyword) for keyword in keywords])
            whoosh_results = searcher.search(q, limit=k)
            doc_ids = [hit["id"] for hit in whoosh_results]
            doc_chunks = [hit["chunks"].split("\n") for hit in whoosh_results]
            doc_vectors = [hit["vectors"] for hit in whoosh_results]
            
            results = []
            for doc_id, chunks, vectors in zip(doc_ids, doc_chunks, doc_vectors):
                for chunk, vector in zip(chunks, vectors):
                    results.append((doc_id, chunk, vector))

        embedder = SentenceTransformer(self.model_name)
        query_vector = torch.tensor(embedder.encode([query])[0])
        unique_docs = set()
        vector_results = []
        for doc_id, chunk, vector in results:
            if doc_id not in unique_docs:
                chunk_vector = torch.tensor(vector)
                similarity = float(torch.nn.functional.cosine_similarity(query_vector, chunk_vector, dim=0))
                vector_results.append((doc_id, chunk, similarity))
                unique_docs.add(doc_id)
                if len(unique_docs) >= k:
                    break

        sorted_results = sorted(vector_results, key=lambda x: x[2], reverse=True)[:k*m]
        
        cross_encode = CrossEncoder()
        ranked_results = cross_encode.rank(query, [result[1] for result in sorted_results])

        return [(doc_id, chunk, score) for (doc_id, chunk, _), score in zip(sorted_results, ranked_results)]

if __name__ == "__main__":
    db = Database()
    db.create()
    
    documents = [
        {"content": "This is a test document."},
        {"content": "This is another test document."}
    ]
    db.add(documents)
    
    results = db.search("test")
    for doc_id, chunk, vector in results:
        print(f"Document ID: {doc_id}")
        print(f"Chunk: {chunk}")
        print(f"Vector: {vector}")
        print("---")
    
    # Create a RAG instance with default values
    # rag = RAG()
    
    # Build the RAG instance with the created database
    # rag.build(db)
    
    # Customize the RAG instance (optional)
    # rag.customize(name="RAG Genius", role="assistant", goal="answer questions in a helpful manner", tone="friendly")
    
    # Invoke the RAG instance with a query
    # query = "What is a test document?"
    # response = rag.invoke(query)
    # print(response) 