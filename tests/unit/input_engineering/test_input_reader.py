from unittest.mock import MagicMock, patch

from documentassistent.input_engineering.input_reader import ImageReader, PDFReader
from documentassistent.structure.state import Document


def test_pdf_reader_reads_pdf() -> None:
    pdf_reader = PDFReader()
    mock_page = MagicMock()
    mock_page.extract_text.return_value = "PDF page text"
    mock_pdf_reader = MagicMock()
    mock_pdf_reader.pages = [mock_page]
    with (
        patch("PyPDF2.PdfReader", return_value=mock_pdf_reader),
        patch("pathlib.Path.open", MagicMock()),
    ):
        doc = pdf_reader.read("dummy.pdf")
    assert isinstance(doc, Document)
    assert doc.content == "PDF page text"
    assert doc.metadata is not None
    assert doc.metadata["type"] == "pdf"


def test_image_reader_reads_image() -> None:
    image_reader = ImageReader()
    mock_image = MagicMock()
    with (
        patch("PIL.Image.open", return_value=mock_image),
        patch(
            "pytesseract.image_to_string",
            return_value="Image text",
        ),
    ):
        doc = image_reader.read("dummy.jpg")
    assert isinstance(doc, Document)
    assert doc.content == "Image text"
    assert doc.metadata is not None
    assert doc.metadata["type"] == "image"
