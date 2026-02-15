# Document Assistant

![Status: Work in Progress](https://img.shields.io/badge/Status-Work%20In%20Progress-yellow)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Tests](https://img.shields.io/github/actions/workflow/status/HeddaZa/GraphRAG/python-quality.yml)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
![Made with](https://img.shields.io/badge/Made%20with-LangChain-orange)

This will be my document assistant. At some point. So it's work in progress.

Eventually, I will just put a photo or pdf of my document into the data folder and run the pipeline. Some LLM agent system will classify my document and extract the most important stuff. These will be saved into a SQLite database (initially planned for Neo4j, but SQLite is simpler for now).
Next time I do my tax return, I can query my database.

I use Ollama but coded an OpenAI option. However, I realised my credit at OpenAI expired, so I didn't test the code. If you want to use OpenAI, be prepared for potential bugs. Feel free to help me out.

!!!THIS IS WORK IN PROGRESS!!!!

## Quick Start

### Installation
1. Install [Poetry](https://python-poetry.org/docs/#installation) if you don't have it
2. Clone this repo
3. Install dependencies:
```bash
poetry install
source .venv/bin/activate
```

### Setup Ollama
* Download Ollama (https://ollama.com/download/mac) and install it
* Start Ollama: `ollama serve`
* Pull the model: `ollama pull gemma:7b`
* If you use a different model, adjust name in `config.yaml`

### (Optional) Setup LangFuse
Set up LangFuse:
* Clone repo: https://github.com/langfuse/langfuse.git
* Build and start the LangFuse docker container
* Instructions: https://langfuse.com/self-hosting/docker-compose

If Langfuse is not set up, warnings will be issued but pipeline will work

### Configuration
Edit `config.yaml` to customize:
* LLM provider (ollama/openai)
* Model name and parameters
* Data paths
* Database location

### Running It
```bash
python main.py
```

This will process example files from `data/pdfs/` and `data/Pictures/`. Or modify `main.py` to point to your own files.

## How It Works

The pipeline uses LangGraph agents to process documents:

1. **Classification Agent** - Figures out what type of document it is (invoice, note, etc.)
2. **Extraction Agent** - Pulls out the important bits based on document type:
   - **Invoice Agent** - Extracts vendor, amounts, dates
   - **Note Agent** - Extracts key points and summaries
3. **Result Agent** - Structures the extracted data
4. **Storage Agent** - Saves everything to SQLite

All of this happens automatically once you run the pipeline. The agents communicate through a state machine built with LangGraph.

## Project Structure

```
documentassistent/
├── agents/           # LangGraph agents for classification and extraction
├── config/           # Configuration management
├── input_engineering/ # PDF and image readers (uses pytesseract for OCR)
├── llm/              # LLM factory supporting Ollama and OpenAI
├── prompts/          # YAML prompt templates
├── storage/          # SQLAlchemy models and repository pattern
├── structure/        # Pydantic models for LLM responses
└── utils/            # Logger, Langfuse integration, file management
```

## Development

### Code Quality
This project uses:
* **ruff** for linting and formatting
* **mypy** for type checking
* **pytest** for testing

Run the checks:
```bash
ruff check .
ruff format .
mypy .
pytest
```


### Testing
```bash
# Run all tests
pytest

# With coverage
pytest --cov=documentassistent --cov-report=html
```

Tests are split into:
* `tests/unit/` - Unit tests for individual components
* `tests/integration/` - End-to-end workflow tests

## Project Status
- [x] Basic LLM integration
- [x] Ollama support
- [ ] OpenAI integration (coded but untested - no credits left!)
- [x] Langfuse tracking with docker
- [x] LangGraph agent system for classification
- [x] Image classification (OCR with pytesseract)
- [x] PDF classification
- [x] Full pipeline from document to SQLite DB
- [x] Invoice extraction
- [x] Note extraction
- [ ] Optional: GraphRAG (was initial plan but is now optional)
- [ ] Optional: Tax return query system
- [ ] Optional: RAG for tax information

## Contributing

Feel free to open issues or PRs! Check out the coding standards in `.github/copilot-instructions.md` before contributing.


