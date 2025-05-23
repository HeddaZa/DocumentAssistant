# Document Assistant

![Status: Work in Progress](https://img.shields.io/badge/Status-Work%20In%20Progress-yellow)

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
- [ ] Neo4j setup
- [ ] Document classification
- [ ] pipeline from document to graphDB entry
- [ ] Tax return query system

