"""Prompt collection loaded from YAML configuration files."""

from documentassistent.prompts.prompt_loader import get_prompt, load_prompt_config

# Load prompts from YAML files
CATEGORISATION_PROMPT = get_prompt("categorisation", text="{text}")
INVOICE_EXTRACTION_PROMPT = load_prompt_config("invoice_extraction")["system"]
NOTE_EXTRACTION_PROMPT = load_prompt_config("note_extraction")["system"]
RESULT_EXTRACTION_PROMPT = load_prompt_config("result_extraction")["system"]
