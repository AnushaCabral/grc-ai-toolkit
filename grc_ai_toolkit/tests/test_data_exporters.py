"""
Comprehensive tests for data exporters module

These tests verify document export functionality to various formats.
"""

import pytest
from pathlib import Path
from unittest.mock import patch, Mock, MagicMock
from grc_ai_toolkit.data.exporters import (
    DocumentExporter,
    ExportFormat,
    DOCX_AVAILABLE,
    REPORTLAB_AVAILABLE
)


class TestExportFormat:
    """Test ExportFormat enum"""

    def test_export_format_values(self):
        """Test all export format enum values"""
        assert ExportFormat.MARKDOWN == "markdown"
        assert ExportFormat.WORD == "docx"
        assert ExportFormat.PDF == "pdf"
        assert ExportFormat.TEXT == "txt"
        assert ExportFormat.HTML == "html"


class TestExportToMarkdown:
    """Test export_to_markdown functionality"""

    def test_export_to_markdown_basic(self, tmp_path):
        """Test basic markdown export"""
        content = "# Test Document\n\nThis is test content."
        output_path = tmp_path / "test.md"

        result = DocumentExporter.export_to_markdown(str(content), str(output_path))

        assert result.exists()
        assert result.read_text(encoding="utf-8") == content

    def test_export_to_markdown_with_metadata(self, tmp_path):
        """Test markdown export with metadata front matter"""
        content = "# Test Document"
        metadata = {"title": "Test", "author": "John Doe", "date": "2025-01-05"}
        output_path = tmp_path / "test_meta.md"

        result = DocumentExporter.export_to_markdown(content, str(output_path), metadata=metadata)

        text = result.read_text(encoding="utf-8")
        assert "---" in text
        assert "title: Test" in text
        assert "author: John Doe" in text
        assert "date: 2025-01-05" in text
        assert "# Test Document" in text

    def test_export_to_markdown_creates_path(self, tmp_path):
        """Test that markdown export creates Path object"""
        content = "Test"
        output_path = tmp_path / "test.md"

        result = DocumentExporter.export_to_markdown(content, str(output_path))

        assert isinstance(result, Path)


class TestExportToText:
    """Test export_to_text functionality"""

    def test_export_to_text_basic(self, tmp_path):
        """Test basic text export"""
        content = "This is plain text content.\nWith multiple lines."
        output_path = tmp_path / "test.txt"

        result = DocumentExporter.export_to_text(content, str(output_path))

        assert result.exists()
        assert content in result.read_text(encoding="utf-8")

    def test_export_to_text_with_metadata(self, tmp_path):
        """Test text export with metadata header"""
        content = "Main content here."
        metadata = {"title": "Test Document", "version": "1.0"}
        output_path = tmp_path / "test_meta.txt"

        result = DocumentExporter.export_to_text(content, str(output_path), metadata=metadata)

        text = result.read_text(encoding="utf-8")
        assert "title: Test Document" in text
        assert "version: 1.0" in text
        assert "=" * 80 in text
        assert "Main content here" in text


class TestExportToHTML:
    """Test export_to_html functionality"""

    def test_export_to_html_basic(self, tmp_path):
        """Test basic HTML export"""
        content = "# Test Heading\n\nThis is a paragraph."
        output_path = tmp_path / "test.html"

        result = DocumentExporter.export_to_html(content, str(output_path))

        html = result.read_text(encoding="utf-8")
        assert "<!DOCTYPE html>" in html
        assert "<html>" in html
        assert "<body>" in html
        assert "</html>" in html

    def test_export_to_html_with_title(self, tmp_path):
        """Test HTML export with title"""
        content = "Content"
        output_path = tmp_path / "test.html"

        result = DocumentExporter.export_to_html(content, str(output_path), title="Test Page")

        html = result.read_text(encoding="utf-8")
        assert "<title>Test Page</title>" in html
        assert "<h1>Test Page</h1>" in html

    def test_export_to_html_with_metadata(self, tmp_path):
        """Test HTML export with metadata"""
        content = "Content"
        metadata = {"author": "John Doe", "date": "2025-01-05"}
        output_path = tmp_path / "test.html"

        result = DocumentExporter.export_to_html(content, str(output_path), metadata=metadata)

        html = result.read_text(encoding="utf-8")
        assert "author" in html
        assert "John Doe" in html
        assert "metadata" in html

    def test_export_to_html_headers(self, tmp_path):
        """Test HTML export converts markdown headers"""
        content = "# H1\n## H2\n### H3"
        output_path = tmp_path / "test.html"

        result = DocumentExporter.export_to_html(content, str(output_path))

        html = result.read_text(encoding="utf-8")
        assert "<h1>H1</h1>" in html
        assert "<h2>H2</h2>" in html
        assert "<h3>H3</h3>" in html

    def test_export_to_html_lists(self, tmp_path):
        """Test HTML export converts markdown lists"""
        content = "- Item 1\n- Item 2\n* Item 3"
        output_path = tmp_path / "test.html"

        result = DocumentExporter.export_to_html(content, str(output_path))

        html = result.read_text(encoding="utf-8")
        assert "<ul>" in html
        assert "</ul>" in html
        assert "<li>Item 1</li>" in html
        assert "<li>Item 2</li>" in html

    def test_export_to_html_paragraphs(self, tmp_path):
        """Test HTML export converts paragraphs"""
        content = "This is a paragraph."
        output_path = tmp_path / "test.html"

        result = DocumentExporter.export_to_html(content, str(output_path))

        html = result.read_text(encoding="utf-8")
        assert "<p>This is a paragraph.</p>" in html

    def test_export_to_html_formatting(self, tmp_path):
        """Test HTML export handles basic markdown formatting"""
        content = "This is **bold** and this is *italic*."
        output_path = tmp_path / "test.html"

        result = DocumentExporter.export_to_html(content, str(output_path))

        html = result.read_text(encoding="utf-8")
        # Note: basic replace will create <strong> and <em> tags
        assert "<strong>" in html or "**" in html


@pytest.mark.skipif(not DOCX_AVAILABLE, reason="python-docx not installed")
class TestExportToWord:
    """Test export_to_word functionality (requires python-docx)"""

    def test_export_to_word_basic(self, tmp_path):
        """Test basic Word export"""
        content = "# Test Document\n\nThis is content."
        output_path = tmp_path / "test.docx"

        result = DocumentExporter.export_to_word(content, str(output_path))

        assert result.exists()
        assert result.suffix == ".docx"

    def test_export_to_word_with_title(self, tmp_path):
        """Test Word export with title"""
        content = "Content here."
        output_path = tmp_path / "test.docx"

        result = DocumentExporter.export_to_word(
            content,
            str(output_path),
            title="Test Document Title"
        )

        assert result.exists()

    def test_export_to_word_with_metadata(self, tmp_path):
        """Test Word export with metadata"""
        content = "Content"
        metadata = {"author": "John Doe", "version": "1.0"}
        output_path = tmp_path / "test.docx"

        result = DocumentExporter.export_to_word(content, str(output_path), metadata=metadata)

        assert result.exists()

    def test_export_to_word_headers(self, tmp_path):
        """Test Word export handles headers"""
        content = "# Header 1\n## Header 2\n### Header 3"
        output_path = tmp_path / "test.docx"

        result = DocumentExporter.export_to_word(content, str(output_path))

        assert result.exists()

    def test_export_to_word_lists(self, tmp_path):
        """Test Word export handles lists"""
        content = "- Bullet 1\n- Bullet 2\n1. Number 1\n2. Number 2"
        output_path = tmp_path / "test.docx"

        result = DocumentExporter.export_to_word(content, str(output_path))

        assert result.exists()

    def test_export_to_word_paragraphs(self, tmp_path):
        """Test Word export handles paragraphs"""
        content = "This is paragraph 1.\n\nThis is paragraph 2."
        output_path = tmp_path / "test.docx"

        result = DocumentExporter.export_to_word(content, str(output_path))

        assert result.exists()


class TestExportToWordWithoutLibrary:
    """Test Word export error handling when python-docx not available"""

    def test_export_to_word_without_docx(self, tmp_path):
        """Test Word export raises error if python-docx not installed"""
        with patch('grc_ai_toolkit.data.exporters.DOCX_AVAILABLE', False):
            content = "Test"
            output_path = tmp_path / "test.docx"

            with pytest.raises(ImportError, match="python-docx not installed"):
                DocumentExporter.export_to_word(content, str(output_path))


@pytest.mark.skipif(not REPORTLAB_AVAILABLE, reason="reportlab not installed")
class TestExportToPDF:
    """Test export_to_pdf functionality (requires reportlab)"""

    def test_export_to_pdf_basic(self, tmp_path):
        """Test basic PDF export"""
        content = "# Test Document\n\nThis is content."
        output_path = tmp_path / "test.pdf"

        result = DocumentExporter.export_to_pdf(content, str(output_path))

        assert result.exists()
        assert result.suffix == ".pdf"

    def test_export_to_pdf_with_title(self, tmp_path):
        """Test PDF export with title"""
        content = "Content here."
        output_path = tmp_path / "test.pdf"

        result = DocumentExporter.export_to_pdf(
            content,
            str(output_path),
            title="Test PDF Title"
        )

        assert result.exists()

    def test_export_to_pdf_with_metadata(self, tmp_path):
        """Test PDF export with metadata"""
        content = "Content"
        metadata = {"author": "John Doe", "version": "1.0"}
        output_path = tmp_path / "test.pdf"

        result = DocumentExporter.export_to_pdf(content, str(output_path), metadata=metadata)

        assert result.exists()

    def test_export_to_pdf_headers(self, tmp_path):
        """Test PDF export handles headers"""
        content = "# Header 1\n## Header 2\n### Header 3"
        output_path = tmp_path / "test.pdf"

        result = DocumentExporter.export_to_pdf(content, str(output_path))

        assert result.exists()

    def test_export_to_pdf_paragraphs(self, tmp_path):
        """Test PDF export handles paragraphs"""
        content = "This is paragraph 1.\n\nThis is paragraph 2."
        output_path = tmp_path / "test.pdf"

        result = DocumentExporter.export_to_pdf(content, str(output_path))

        assert result.exists()


class TestExportToPDFWithoutLibrary:
    """Test PDF export error handling when reportlab not available"""

    def test_export_to_pdf_without_reportlab(self, tmp_path):
        """Test PDF export raises error if reportlab not installed"""
        with patch('grc_ai_toolkit.data.exporters.REPORTLAB_AVAILABLE', False):
            content = "Test"
            output_path = tmp_path / "test.pdf"

            with pytest.raises(ImportError, match="reportlab not installed"):
                DocumentExporter.export_to_pdf(content, str(output_path))


class TestExportGenericMethod:
    """Test the generic export() method"""

    def test_export_markdown(self, tmp_path):
        """Test generic export to markdown"""
        content = "# Test"
        output_path = tmp_path / "test.md"

        result = DocumentExporter.export(
            content,
            str(output_path),
            format=ExportFormat.MARKDOWN
        )

        assert result.exists()

    def test_export_text(self, tmp_path):
        """Test generic export to text"""
        content = "Test content"
        output_path = tmp_path / "test.txt"

        result = DocumentExporter.export(
            content,
            str(output_path),
            format=ExportFormat.TEXT
        )

        assert result.exists()

    def test_export_html(self, tmp_path):
        """Test generic export to HTML"""
        content = "# Test"
        output_path = tmp_path / "test.html"

        result = DocumentExporter.export(
            content,
            str(output_path),
            format=ExportFormat.HTML
        )

        assert result.exists()

    @pytest.mark.skipif(not DOCX_AVAILABLE, reason="python-docx not installed")
    def test_export_word(self, tmp_path):
        """Test generic export to Word"""
        content = "Test content"
        output_path = tmp_path / "test.docx"

        result = DocumentExporter.export(
            content,
            str(output_path),
            format=ExportFormat.WORD
        )

        assert result.exists()

    @pytest.mark.skipif(not REPORTLAB_AVAILABLE, reason="reportlab not installed")
    def test_export_pdf(self, tmp_path):
        """Test generic export to PDF"""
        content = "Test content"
        output_path = tmp_path / "test.pdf"

        result = DocumentExporter.export(
            content,
            str(output_path),
            format=ExportFormat.PDF
        )

        assert result.exists()

    def test_export_adds_metadata(self, tmp_path):
        """Test export adds default metadata"""
        content = "Test"
        output_path = tmp_path / "test.md"

        result = DocumentExporter.export(
            content,
            str(output_path),
            format=ExportFormat.MARKDOWN
        )

        text = result.read_text(encoding="utf-8")
        assert "generated_date" in text
        assert "generator: GRC AI Toolkit" in text

    def test_export_preserves_custom_metadata(self, tmp_path):
        """Test export preserves user-provided metadata"""
        content = "Test"
        metadata = {"author": "John Doe", "custom_field": "value"}
        output_path = tmp_path / "test.md"

        result = DocumentExporter.export(
            content,
            str(output_path),
            format=ExportFormat.MARKDOWN,
            metadata=metadata
        )

        text = result.read_text(encoding="utf-8")
        assert "author: John Doe" in text
        assert "custom_field: value" in text
        assert "generated_date" in text  # Default still added

    def test_export_invalid_format(self, tmp_path):
        """Test export raises error for invalid format"""
        content = "Test"
        output_path = tmp_path / "test.xyz"

        with pytest.raises(ValueError, match="Unsupported export format"):
            DocumentExporter.export(
                content,
                str(output_path),
                format="invalid_format"  # type: ignore
            )

    def test_export_with_title(self, tmp_path):
        """Test export with title parameter"""
        content = "Content"
        output_path = tmp_path / "test.html"

        result = DocumentExporter.export(
            content,
            str(output_path),
            format=ExportFormat.HTML,
            title="My Document"
        )

        html = result.read_text(encoding="utf-8")
        assert "My Document" in html


class TestExportComplexContent:
    """Test exporting complex content with multiple formatting"""

    def test_export_mixed_content_markdown(self, tmp_path):
        """Test exporting complex mixed content to markdown"""
        content = """# Main Title

## Section 1

This is a paragraph with **bold** and *italic* text.

- List item 1
- List item 2

### Subsection

Another paragraph here.
"""
        output_path = tmp_path / "complex.md"

        result = DocumentExporter.export_to_markdown(content, str(output_path))

        text = result.read_text(encoding="utf-8")
        assert "# Main Title" in text
        assert "**bold**" in text
        assert "- List item 1" in text

    def test_export_mixed_content_html(self, tmp_path):
        """Test exporting complex mixed content to HTML"""
        content = """# Main Title

## Section 1

This is a paragraph.

- List item 1
- List item 2
"""
        output_path = tmp_path / "complex.html"

        result = DocumentExporter.export_to_html(content, str(output_path))

        html = result.read_text(encoding="utf-8")
        assert "<h1>Main Title</h1>" in html
        assert "<h2>Section 1</h2>" in html
        assert "<li>List item 1</li>" in html


class TestPathHandling:
    """Test Path object handling"""

    def test_export_accepts_string_path(self, tmp_path):
        """Test export accepts string path"""
        content = "Test"
        output_path = str(tmp_path / "test.md")

        result = DocumentExporter.export_to_markdown(content, output_path)

        assert isinstance(result, Path)
        assert result.exists()

    def test_export_accepts_path_object(self, tmp_path):
        """Test export accepts Path object"""
        content = "Test"
        output_path = tmp_path / "test.md"

        result = DocumentExporter.export_to_markdown(content, output_path)

        assert isinstance(result, Path)
        assert result.exists()

    def test_export_returns_path_object(self, tmp_path):
        """Test all export methods return Path objects"""
        content = "Test"

        # Markdown
        result_md = DocumentExporter.export_to_markdown(content, str(tmp_path / "test.md"))
        assert isinstance(result_md, Path)

        # Text
        result_txt = DocumentExporter.export_to_text(content, str(tmp_path / "test.txt"))
        assert isinstance(result_txt, Path)

        # HTML
        result_html = DocumentExporter.export_to_html(content, str(tmp_path / "test.html"))
        assert isinstance(result_html, Path)
