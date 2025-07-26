# Document Assistant

![Status: Work in Progress](https://img.shields.io/badge/Status-Work%20In%20Progress-yellow)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Tests](https://img.shields.io/github/actions/workflow/status/HeddaZa/GraphRAG/python-quality.yml)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
![Made with](https://img.shields.io/badge/Made%20with-LangChain-orange)

This will be my document assistant. At some point. So it's work in progress.

Eventually, I will just put a photo or pdf of my document into the data folder and run the pipeline. Some LLM agent system will classify my document and extract the most important stuff. These will be saved into a graphDB (probably Neo4j).
Next time I do my tax return, I can query my graphDB.

I use Ollama but coded an OpenAI option. However, I realised my credit at OpenAI expired, so I didn't test the code. If you want to use OpenAI, be prepared for potential bugs. Feel free to help me out

!!!THIS IS WORK IN PROGRESS!!!!


### Using Ollama: 
* download Ollama (https://ollama.com/download/mac) and install it
* start Ollama with `ollama serve`
* pull model. Model used here: gemma:7b
* if you use a different model, adjust name in config file

### Using LangFuse:
* clone repo https://github.com/langfuse/langfuse.git
* build and start the LangFuse docker container
* instructions: https://langfuse.com/self-hosting/docker-compose

## Project Status
- [x] Basic LLM integration
- [x] Ollama support
- [ ] OpenAI integration
- [x] Langfuse with docker
- [x] Langgraph Agent System for classification
- [x] Pictures will be classified
- [x] Pdfs will be classified
- [ ] Neo4j setup
- [ ] pipeline from document to graphDB entry
- [ ] optional: graphRAG (was initial plan but is now optional)
- [ ] Tax return query system
- [ ] RAG for tax information

