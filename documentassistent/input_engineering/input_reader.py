from abc import ABC, abstractmethod
from pathlib import Path

from documentassistent.exceptions import (
    FileReadError,
    ThisFileNotFoundError,
)
from documentassistent.structure.state import Document


class DocumentReader(ABC):
    """Abstract base class for document readers."""

    @abstractmethod
    def read(self, path: str) -> Document:
        """Read a document from the given file path."""


class PDFReader(DocumentReader):
    """Reads PDF files and extracts their text content into Document objects."""

    def read(self, path: str) -> Document:
        """Read a PDF file and extract its text content into a Document object."""
        import PyPDF2

        file_path = Path(path)
        if not file_path.exists():
            msg = f"PDF file not found: {path}"
            raise ThisFileNotFoundError(msg)

        try:
            content = ""
            with file_path.open("rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    content += page.extract_text() or ""
            return Document(content=content, metadata={"source": path, "type": "pdf"})
        except Exception as e:
            msg = f"Failed to read PDF file: {path}"
            raise FileReadError(msg) from e


class ImageReader(DocumentReader):
    """Reads image files and extracts their text content into Document objects."""

    def read(self, path: str) -> Document:
        """Read an image file and extract its text content into a Document object."""
        import pytesseract
        from PIL import Image

        file_path = Path(path)
        if not file_path.exists():
            msg = f"Image file not found: {path}"
            raise ThisFileNotFoundError(msg)

        try:
            image = Image.open(path)
            content = pytesseract.image_to_string(image)
            return Document(content=content, metadata={"source": path, "type": "image"})
        except Exception as e:
            msg = f"Failed to read image file: {path}"
            raise FileReadError(msg) from e


if __name__ == "__main__":
    from pathlib import Path

    path_pdfs = list(Path("data/pdfs/").glob("*.pdf"))
    paths_pictures = list(Path("data/Pictures/").glob("*.jpg"))

    pdf_reader = PDFReader()
    pdf_doc = pdf_reader.read(str(path_pdfs[0]))

    image_reader = ImageReader()
    image_doc = image_reader.read(str(paths_pictures[0]))
