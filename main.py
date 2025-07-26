from pathlib import Path

from dotenv import load_dotenv

from documentassistent.graph import create_graph
from documentassistent.input_engineering.input_reader import ImageReader, PDFReader
from documentassistent.prompts.prompt_collection import CATEGORISATION_PROMPT
from documentassistent.structure.state import State
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
        logger.info("PDF file processed", extra={"file_path": str(path)})
    elif path.suffix.lower() in [".png", ".jpg", ".jpeg"]:
        reader_image = ImageReader()
        text = reader_image.read(str(path)).content
        logger.info("Image file processed", extra={"file_path": str(path)})
    else:
        logger.error("Unsupported file type", extra={"file_suffix": path.suffix})
        return

    state = State(
        prompt=CATEGORISATION_PROMPT,
        text=text,
        result=None,
    )
    graph = create_graph()
    result = graph.invoke(state)
    logger.debug("Final state after processing: {}", result)


if __name__ == "__main__":
    path_pdfs = list(Path("data/pdfs/").glob("*.pdf"))
    paths_pictures = list(Path("data/Pictures/").glob("*.jpg"))

    main(path=path_pdfs[0])

    main(path=paths_pictures[0])
