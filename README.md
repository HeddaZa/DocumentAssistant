# Document Assistant

![Status: Work in Progress](https://img.shields.io/badge/Status-Work%20In%20Progress-yellow)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Tests](https://img.shields.io/github/actions/workflow/status/HeddaZa/DocumentAssistant/python-quality.yml)
[![Code Coverage](https://codecov.io/gh/HeddaZa/DocumentAssistant/branch/main/graph/badge.svg)](https://codecov.io/gh/HeddaZa/DocumentAssistant)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
![Made with](https://img.shields.io/badge/Made%20with-LangChain-orange)

This will be my document assistant. At some point. So it's work in progress.

Eventually, I will just put a photo or pdf of my document into the data folder and run the pipeline. Some LLM agent system will classify my document and extract the most important stuff. These will be saved into a graphDB (probably Neo4j).
Next time I do my tax return, I can query my graphDB.

I use Ollama but coded an OpenAI option. However, I realised my credit at OpenAI expired, so I didn't test the code. If you want to use OpenAI, be prepared for potential bugs. Feel free to help me out

!!!THIS IS WORK IN PROGRESS!!!!


### Using Ollama: 
* download Ollama
* start Ollama with `ollama serve`
* pull model. Model used here: gemma:7b
* if you use a different model, adjust name in config file

## Project Status
- [x] Basic LLM integration
- [x] Ollama support
- [ ] OpenAI integration
- [ ] Langfuse with docker
- [ ] Pictures will be classified
- [ ] Pdfs will be classified
- [ ] Neo4j setup
- [ ] pipeline from document to graphDB entry
- [ ] Tax return query system

