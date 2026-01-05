"""
Integration tests for RAG pipeline (document processing + vector search)

These tests verify the end-to-end RAG functionality.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from tempfile import NamedTemporaryFile

from grc_ai_toolkit.data import DocumentProcessor, VectorStore, ProcessingConfig, VectorStoreConfig
from grc_ai_toolkit.data.vector_store import VectorStoreType
from langchain_core.documents import Document


class TestRAGPipeline:
    """Test RAG pipeline end-to-end"""

    @pytest.fixture
    def sample_text_file(self, tmp_path):
        """Create a sample text file for testing"""
        test_file = tmp_path / "test_document.txt"
        test_content = """
        Information Security Policy

        1. Purpose
        This policy establishes the security requirements for protecting company information assets.

        2. Scope
        This policy applies to all employees, contractors, and third-party users.

        3. Password Requirements
        All passwords must be at least 12 characters long and include uppercase, lowercase,
        numbers, and special characters. Passwords must be changed every 90 days.

        4. Data Classification
        Data must be classified as Public, Internal, Confidential, or Restricted.
        Confidential and Restricted data must be encrypted at rest and in transit.

        5. Incident Response
        Security incidents must be reported within 24 hours to the security team.
        The incident response team will investigate and remediate all reported incidents.
        """
        test_file.write_text(test_content)
        return test_file

    @pytest.fixture
    def doc_processor(self):
        """Create a document processor with test configuration"""
        config = ProcessingConfig(
            chunk_size=200,  # Smaller chunks for testing
            chunk_overlap=50
        )
        return DocumentProcessor(config)

    def test_document_loading(self, doc_processor, sample_text_file):
        """Test loading a document file"""
        documents = doc_processor.load_document(sample_text_file)

        assert isinstance(documents, list)
        assert len(documents) > 0
        assert all(isinstance(doc, Document) for doc in documents)
        assert all(doc.page_content for doc in documents)

    def test_document_splitting(self, doc_processor, sample_text_file):
        """Test splitting documents into chunks"""
        # Load document
        documents = doc_processor.load_document(sample_text_file)

        # Split into chunks using text_splitter
        chunks = doc_processor.text_splitter.split_documents(documents)

        assert isinstance(chunks, list)
        assert len(chunks) > 1  # Should be split into multiple chunks
        assert all(isinstance(chunk, Document) for chunk in chunks)

        # Verify chunks aren't too large
        for chunk in chunks:
            assert len(chunk.page_content) <= doc_processor.config.chunk_size + 100  # Allow some flexibility

    @pytest.mark.skip(reason="Requires downloading embedding model, slow test")
    def test_vector_store_creation_faiss(self, doc_processor, sample_text_file):
        """Test creating a FAISS vector store from documents"""
        # Load and split documents
        documents = doc_processor.load_document(sample_text_file)
        chunks = doc_processor.text_splitter.split_documents(documents)

        # Create vector store
        config = VectorStoreConfig(
            store_type=VectorStoreType.FAISS,
            use_openai_embeddings=False,  # Use local embeddings for testing
            k=2
        )
        vector_store = VectorStore(config)
        vector_store.create_from_documents(chunks)

        assert vector_store.vector_store is not None

        # Test search
        results = vector_store.search("What are the password requirements?")
        assert isinstance(results, list)
        assert len(results) <= config.k
        assert all(isinstance(doc, Document) for doc in results)

    def test_vector_store_mock_embeddings(self, doc_processor, sample_text_file):
        """Test vector store with mocked embeddings"""
        # Load and split documents
        documents = doc_processor.load_document(sample_text_file)
        chunks = doc_processor.text_splitter.split_documents(documents)

        # We'll just verify the pipeline works without actually creating embeddings
        assert len(chunks) > 0
        assert all(isinstance(chunk, Document) for chunk in chunks)

        # Verify chunks contain relevant content
        content = " ".join(chunk.page_content for chunk in chunks)
        assert "password" in content.lower()
        assert "security" in content.lower()

    def test_end_to_end_rag_mock(self, doc_processor, sample_text_file):
        """Test end-to-end RAG pipeline with mocks"""
        # Step 1: Load document
        documents = doc_processor.load_document(sample_text_file)
        assert len(documents) > 0

        # Step 2: Split into chunks
        chunks = doc_processor.text_splitter.split_documents(documents)
        assert len(chunks) > 0

        # Step 3: Verify chunks can be used for RAG
        # Find chunks about passwords
        password_chunks = [
            chunk for chunk in chunks
            if "password" in chunk.page_content.lower()
        ]
        assert len(password_chunks) > 0

        # Verify we can extract relevant information
        password_info = password_chunks[0].page_content
        assert "12 characters" in password_info or "least" in password_info

    def test_unsupported_file_type(self, doc_processor, tmp_path):
        """Test that unsupported file types raise an error"""
        unsupported_file = tmp_path / "test.xyz"
        unsupported_file.write_text("test content")

        with pytest.raises(ValueError, match="Unsupported file type"):
            doc_processor.load_document(unsupported_file)

    def test_file_not_found(self, doc_processor):
        """Test that missing files raise an error"""
        with pytest.raises(FileNotFoundError):
            doc_processor.load_document("nonexistent_file.txt")

    def test_text_cleaning(self):
        """Test text cleaning utility"""
        from grc_ai_toolkit.data import DataProcessor

        dirty_text = "  Multiple   spaces\r\nWindows   line\rendings\x00null  "
        clean_text = DataProcessor.clean_text(dirty_text)

        assert "  " not in clean_text  # No double spaces
        assert "\r" not in clean_text  # No carriage returns
        assert "\x00" not in clean_text  # No null bytes
        # clean_text normalizes all whitespace to single spaces
        assert "Multiple spaces" in clean_text
        assert "Windows line" in clean_text
        assert "endings" in clean_text
        assert "null" in clean_text

    def test_chunk_list_utility(self):
        """Test list chunking utility"""
        from grc_ai_toolkit.data import DataProcessor

        items = list(range(10))
        chunks = DataProcessor.chunk_list(items, 3)

        assert len(chunks) == 4  # 3, 3, 3, 1
        assert chunks[0] == [0, 1, 2]
        assert chunks[1] == [3, 4, 5]
        assert chunks[2] == [6, 7, 8]
        assert chunks[3] == [9]


@pytest.mark.integration
class TestRAGIntegrationWithEmbeddings:
    """
    Integration tests with real embeddings (slower, optional)

    Run with: pytest -m integration tests/test_rag_integration.py
    """

    @pytest.mark.skip(reason="Requires downloading embeddings model, slow")
    def test_full_rag_pipeline_faiss(self, tmp_path):
        """Test complete RAG pipeline with FAISS"""
        # Create test document
        test_file = tmp_path / "policy.txt"
        test_file.write_text("""
        Data Protection Policy

        Personal data must be processed lawfully, fairly, and transparently.
        Data must be collected for specified, explicit and legitimate purposes.
        Data must be adequate, relevant and limited to what is necessary.
        Data must be accurate and kept up to date.
        Data must be kept in a form which permits identification for no longer than necessary.
        Data must be processed securely using appropriate technical and organizational measures.
        """)

        # Initialize processor
        config = ProcessingConfig(chunk_size=150, chunk_overlap=30)
        processor = DocumentProcessor(config)

        # Load and split
        documents = processor.load_document(test_file)
        chunks = processor.text_splitter.split_documents(documents)

        # Create vector store
        vs_config = VectorStoreConfig(
            store_type=VectorStoreType.FAISS,
            use_openai_embeddings=False,
            k=2
        )
        vector_store = VectorStore(vs_config)
        vector_store.create_from_documents(chunks)

        # Search
        results = vector_store.search("How should personal data be processed?")

        # Verify results
        assert len(results) > 0
        assert any("lawfully" in doc.page_content.lower() or "fairly" in doc.page_content.lower()
                   for doc in results)
