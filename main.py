from pathlib import Path

from dotenv import load_dotenv

from documentassistent.input_engineering.input_reader import ImageReader, PDFReader
from documentassistent.llm.llm_factory import ConfigDict, LLMFactory
from documentassistent.prompts.prompt_collection import CATEGORISATION_PROMPT
from documentassistent.structure.pydantic_llm_calls.invoice_call import DocumentType
from documentassistent.structure.state import State
from documentassistent.utils.logger import setup_logger
from load_config import load_config

load_dotenv()

logger = setup_logger(name="MyApp", log_file="logs/app.log")
CONFIG = load_config("config.yaml")


def main(path: Path) -> None:
    """Load configuration and process text with LLM."""
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

    config: ConfigDict = {
        "llm": {
            "type": "ollama",
            "model": CONFIG["ollama"]["model"],
        },
    }

    llm = LLMFactory.create_llm(config)
    logger.info("LLM instance created", extra={"llm_type": type(llm).__name__})

    state = State(
        prompt=CATEGORISATION_PROMPT,
        text=text,
        result=None,
    )
    result = llm.call(state, pydantic_object=DocumentType)
    logger.debug("Full result details: {}", result)


if __name__ == "__main__":
    path_pdfs = list(Path("data/pdfs/").glob("*.pdf"))
    paths_pictures = list(Path("data/Pictures/").glob("*.jpg"))

    main(path=path_pdfs[0])
    main(path=paths_pictures[0])
