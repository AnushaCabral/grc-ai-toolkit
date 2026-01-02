"""
Vector Store for RAG (Retrieval-Augmented Generation)
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging
from pathlib import Path

from langchain_community.vectorstores import FAISS, Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document


logger = logging.getLogger(__name__)


class VectorStoreType(str, Enum):
    """Supported vector store types"""

    FAISS = "faiss"
    CHROMA = "chroma"


@dataclass
class VectorStoreConfig:
    """Configuration for vector store"""

    store_type: VectorStoreType = VectorStoreType.FAISS
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    use_openai_embeddings: bool = False
    openai_api_key: Optional[str] = None

    # Search parameters
    k: int = 2  # Number of results (k=2 is optimal per 2025 research)
    search_type: str = "similarity"  # "similarity" or "mmr"
    score_threshold: Optional[float] = None  # Minimum similarity score

    # Storage
    persist_directory: Optional[str] = None


class VectorStore:
    """
    Vector store for semantic search and RAG

    Supports:
    - FAISS (in-memory, fast)
    - ChromaDB (persistent, queryable)

    Features:
    - Document embedding
    - Semantic search
    - Similarity threshold filtering
    - Persistence
    """

    def __init__(self, config: Optional[VectorStoreConfig] = None):
        """
        Initialize vector store

        Args:
            config: Vector store configuration
        """
        self.config = config or VectorStoreConfig()
        self.vector_store = None

        # Initialize embeddings
        if self.config.use_openai_embeddings:
            if not self.config.openai_api_key:
                raise ValueError("OpenAI API key required for OpenAI embeddings")

            self.embeddings = OpenAIEmbeddings(
                openai_api_key=self.config.openai_api_key
            )
            logger.info("Using OpenAI embeddings")
        else:
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.config.embedding_model
            )
            logger.info(f"Using HuggingFace embeddings: {self.config.embedding_model}")

    def create_from_documents(self, documents: List[Document]) -> None:
        """
        Create vector store from documents

        Args:
            documents: List of Document objects
        """
        if not documents:
            raise ValueError("No documents provided")

        logger.info(f"Creating vector store from {len(documents)} documents")

        if self.config.store_type == VectorStoreType.FAISS:
            self.vector_store = FAISS.from_documents(
                documents=documents, embedding=self.embeddings
            )

        elif self.config.store_type == VectorStoreType.CHROMA:
            if not self.config.persist_directory:
                raise ValueError("persist_directory required for ChromaDB")

            self.vector_store = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.config.persist_directory,
            )

        else:
            raise ValueError(f"Unsupported store type: {self.config.store_type}")

        logger.info("Vector store created successfully")

    def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to existing vector store

        Args:
            documents: Documents to add
        """
        if self.vector_store is None:
            raise RuntimeError("Vector store not initialized. Call create_from_documents first.")

        self.vector_store.add_documents(documents)
        logger.info(f"Added {len(documents)} documents to vector store")

    def search(
        self, query: str, k: Optional[int] = None, filters: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Search vector store

        Args:
            query: Search query
            k: Number of results (defaults to config.k)
            filters: Optional metadata filters

        Returns:
            List of matching documents
        """
        if self.vector_store is None:
            raise RuntimeError("Vector store not initialized")

        k = k or self.config.k

        try:
            if self.config.search_type == "similarity":
                results = self.vector_store.similarity_search(
                    query=query, k=k, filter=filters
                )
            elif self.config.search_type == "mmr":
                # Maximal Marginal Relevance for diversity
                results = self.vector_store.max_marginal_relevance_search(
                    query=query, k=k, filter=filters
                )
            else:
                raise ValueError(f"Unknown search type: {self.config.search_type}")

            logger.info(f"Found {len(results)} results for query")

            return results

        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            raise

    def search_with_score(
        self, query: str, k: Optional[int] = None, filters: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[Document, float]]:
        """
        Search with similarity scores

        Args:
            query: Search query
            k: Number of results
            filters: Metadata filters

        Returns:
            List of (Document, score) tuples
        """
        if self.vector_store is None:
            raise RuntimeError("Vector store not initialized")

        k = k or self.config.k

        results = self.vector_store.similarity_search_with_score(
            query=query, k=k, filter=filters
        )

        # Apply score threshold if configured
        if self.config.score_threshold is not None:
            results = [(doc, score) for doc, score in results if score >= self.config.score_threshold]

        logger.info(f"Found {len(results)} results above threshold")

        return results

    def save(self, path: Optional[str] = None) -> None:
        """
        Save vector store to disk

        Args:
            path: Save path (uses config.persist_directory if not provided)
        """
        if self.vector_store is None:
            raise RuntimeError("Vector store not initialized")

        if self.config.store_type == VectorStoreType.FAISS:
            save_path = path or self.config.persist_directory
            if not save_path:
                raise ValueError("Save path required for FAISS")

            self.vector_store.save_local(save_path)
            logger.info(f"Saved FAISS vector store to {save_path}")

        elif self.config.store_type == VectorStoreType.CHROMA:
            # ChromaDB persists automatically if persist_directory is set
            logger.info("ChromaDB vector store persisted automatically")

    def load(self, path: Optional[str] = None) -> None:
        """
        Load vector store from disk

        Args:
            path: Load path
        """
        if self.config.store_type == VectorStoreType.FAISS:
            load_path = path or self.config.persist_directory
            if not load_path:
                raise ValueError("Load path required")

            self.vector_store = FAISS.load_local(
                load_path, embeddings=self.embeddings, allow_dangerous_deserialization=True
            )
            logger.info(f"Loaded FAISS vector store from {load_path}")

        elif self.config.store_type == VectorStoreType.CHROMA:
            if not self.config.persist_directory:
                raise ValueError("persist_directory required for ChromaDB")

            self.vector_store = Chroma(
                persist_directory=self.config.persist_directory,
                embedding_function=self.embeddings,
            )
            logger.info(f"Loaded ChromaDB from {self.config.persist_directory}")

    def delete(self, ids: Optional[List[str]] = None) -> None:
        """
        Delete documents from vector store

        Args:
            ids: Document IDs to delete (if None, deletes all)
        """
        if self.vector_store is None:
            raise RuntimeError("Vector store not initialized")

        if ids:
            self.vector_store.delete(ids)
            logger.info(f"Deleted {len(ids)} documents")
        else:
            # Delete all (reinitialize)
            self.vector_store = None
            logger.info("Deleted all documents")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get vector store statistics

        Returns:
            Statistics dict
        """
        if self.vector_store is None:
            return {"status": "not_initialized"}

        stats = {
            "status": "initialized",
            "store_type": self.config.store_type.value,
            "embedding_model": self.config.embedding_model,
            "k": self.config.k,
            "search_type": self.config.search_type,
        }

        # Try to get document count (FAISS-specific)
        if self.config.store_type == VectorStoreType.FAISS and self.vector_store:
            try:
                stats["document_count"] = self.vector_store.index.ntotal
            except:
                stats["document_count"] = "unknown"

        return stats

    def __repr__(self) -> str:
        status = "initialized" if self.vector_store else "not initialized"
        return f"<VectorStore: {self.config.store_type.value} ({status})>"
