from pathlib import Path

from dotenv import load_dotenv

from documentassistent.input_engineering.input_reader import ImageReader, PDFReader
from documentassistent.pipeline import create_pipeline
from documentassistent.storage import init_database
from documentassistent.structure.state import ClassificationState
from documentassistent.utils.logger import setup_logger
from load_config import load_config

load_dotenv()

logger = setup_logger(name="MyApp", log_file="logs/app.log")
CONFIG = load_config("config.yaml")


def main(path: Path) -> None:
    """Process a file from the given Path using LLM based on its type (PDF or image)."""
    if path.suffix.lower() in [".pdf"]:
        reader_pdf = PDFReader()
        text = reader_pdf.read(str(path)).content
        logger.info("PDF file processed, {}", path)
    elif path.suffix.lower() in [".png", ".jpg", ".jpeg"]:
        reader_image = ImageReader()
        text = reader_image.read(str(path)).content
        logger.info("Image file processed, {}", path)
    else:
        logger.error("Unsupported file type, {}", path.suffix)
        return

    state = ClassificationState(
        text=text,
        file_path=str(path.absolute()),
    )
    pipeline = create_pipeline()
    result = pipeline.invoke(state)
    logger.debug("Final state after processing: {}", result)

    if hasattr(result, "document_id") and result.document_id:
        logger.success(
            "Document processed and stored, ID: {}, Path: {}",
            result.document_id,
            str(path),
        )


if __name__ == "__main__":
    init_database(CONFIG["database"]["path"])

    path_pdfs = list(Path("data/pdfs/").glob("*.pdf"))
    paths_pictures = list(Path("data/Pictures/").glob("*.jpg"))

    main(path=path_pdfs[0])

    main(path=paths_pictures[0])
