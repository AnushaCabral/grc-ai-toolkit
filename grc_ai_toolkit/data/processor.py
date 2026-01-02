"""
Data Processing Utilities
"""

from typing import List, Dict, Any, Optional, Union
from pathlib import Path
import logging
from dataclasses import dataclass

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    CSVLoader,
    UnstructuredHTMLLoader,
)
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
)
from langchain_core.documents import Document


logger = logging.getLogger(__name__)


@dataclass
class ProcessingConfig:
    """Configuration for document processing"""

    chunk_size: int = 1000
    chunk_overlap: int = 200
    separator: str = "\n\n"
    length_function: callable = len


class DataProcessor:
    """
    General data processing utilities

    Provides common data transformation and validation functions.
    """

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize text

        Args:
            text: Input text

        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = " ".join(text.split())

        # Remove special characters that might cause issues
        text = text.replace("\x00", "")

        # Normalize line endings
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        return text.strip()

    @staticmethod
    def validate_json_structure(data: Dict[str, Any], required_fields: List[str]) -> bool:
        """
        Validate JSON structure has required fields

        Args:
            data: JSON data as dict
            required_fields: List of required field names

        Returns:
            True if all fields present
        """
        return all(field in data for field in required_fields)

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename for safe storage

        Args:
            filename: Original filename

        Returns:
            Sanitized filename
        """
        # Remove or replace problematic characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, "_")

        # Limit length
        max_length = 255
        name, ext = filename.rsplit(".", 1) if "." in filename else (filename, "")
        if len(filename) > max_length:
            name = name[: max_length - len(ext) - 1]
            filename = f"{name}.{ext}" if ext else name

        return filename

    @staticmethod
    def chunk_list(items: List[Any], chunk_size: int) -> List[List[Any]]:
        """
        Split list into chunks

        Args:
            items: List to chunk
            chunk_size: Size of each chunk

        Returns:
            List of chunks
        """
        return [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]


class DocumentProcessor:
    """
    Document processing for various file formats

    Supports:
    - PDF
    - Word (DOCX)
    - Text
    - CSV
    - HTML

    Features:
    - Document loading
    - Text extraction
    - Chunking for RAG
    - Metadata extraction
    """

    def __init__(self, config: Optional[ProcessingConfig] = None):
        """
        Initialize document processor

        Args:
            config: Processing configuration
        """
        self.config = config or ProcessingConfig()

        # Text splitter for chunking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
            length_function=self.config.length_function,
        )

        logger.info("DocumentProcessor initialized")

    def load_document(self, file_path: Union[str, Path]) -> List[Document]:
        """
        Load document from file

        Args:
            file_path: Path to document

        Returns:
            List of Document objects

        Raises:
            ValueError: If file type not supported
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Select appropriate loader based on extension
        suffix = file_path.suffix.lower()

        loader_map = {
            ".pdf": PyPDFLoader,
            ".docx": Docx2txtLoader,
            ".txt": TextLoader,
            ".csv": CSVLoader,
            ".html": UnstructuredHTMLLoader,
            ".htm": UnstructuredHTMLLoader,
        }

        if suffix not in loader_map:
            raise ValueError(
                f"Unsupported file type: {suffix}. "
                f"Supported types: {', '.join(loader_map.keys())}"
            )

        loader_class = loader_map[suffix]

        try:
            loader = loader_class(str(file_path))
            documents = loader.load()

            logger.info(f"Loaded {len(documents)} pages/chunks from {file_path.name}")

            return documents

        except Exception as e:
            logger.error(f"Error loading {file_path}: {str(e)}")
            raise

    def process_document(
        self, file_path: Union[str, Path], add_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Load and process document into chunks

        Args:
            file_path: Path to document
            add_metadata: Additional metadata to add to chunks

        Returns:
            List of chunked Document objects
        """
        # Load document
        documents = self.load_document(file_path)

        # Add metadata
        if add_metadata:
            for doc in documents:
                doc.metadata.update(add_metadata)

        # Split into chunks
        chunks = self.text_splitter.split_documents(documents)

        logger.info(f"Split into {len(chunks)} chunks")

        return chunks

    def process_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> List[Document]:
        """
        Process raw text into chunks

        Args:
            text: Input text
            metadata: Metadata for chunks

        Returns:
            List of chunked Document objects
        """
        # Clean text
        text = DataProcessor.clean_text(text)

        # Create document
        doc = Document(page_content=text, metadata=metadata or {})

        # Split into chunks
        chunks = self.text_splitter.split_documents([doc])

        logger.info(f"Split text into {len(chunks)} chunks")

        return chunks

    def extract_text(self, file_path: Union[str, Path]) -> str:
        """
        Extract all text from document

        Args:
            file_path: Path to document

        Returns:
            Extracted text
        """
        documents = self.load_document(file_path)

        # Combine all pages/chunks
        text = "\n\n".join(doc.page_content for doc in documents)

        return DataProcessor.clean_text(text)

    def get_document_stats(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Get statistics about a document

        Args:
            file_path: Path to document

        Returns:
            Statistics dict
        """
        file_path = Path(file_path)
        documents = self.load_document(file_path)

        # Extract text
        text = "\n".join(doc.page_content for doc in documents)

        # Calculate statistics
        stats = {
            "filename": file_path.name,
            "file_size_bytes": file_path.stat().st_size,
            "pages_or_sections": len(documents),
            "total_characters": len(text),
            "total_words": len(text.split()),
            "estimated_tokens": len(text) // 4,  # Rough estimate
        }

        # Chunk statistics
        chunks = self.text_splitter.split_documents(documents)
        stats["total_chunks"] = len(chunks)
        stats["avg_chunk_size"] = sum(len(c.page_content) for c in chunks) // len(chunks)

        return stats

    def batch_process(
        self, file_paths: List[Union[str, Path]], add_metadata: bool = True
    ) -> List[Document]:
        """
        Process multiple documents

        Args:
            file_paths: List of file paths
            add_metadata: Whether to add source metadata

        Returns:
            Combined list of Document chunks
        """
        all_chunks = []

        for file_path in file_paths:
            try:
                metadata = {"source": str(file_path)} if add_metadata else None
                chunks = self.process_document(file_path, add_metadata=metadata)
                all_chunks.extend(chunks)

            except Exception as e:
                logger.error(f"Failed to process {file_path}: {str(e)}")
                continue

        logger.info(
            f"Batch processed {len(file_paths)} files into {len(all_chunks)} total chunks"
        )

        return all_chunks
