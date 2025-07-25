from documentassistent.prompts import prompt_collection


def test_categorisation_prompt_exists() -> None:
    assert isinstance(prompt_collection.CATEGORISATION_PROMPT, str)
    assert "{text}" in prompt_collection.CATEGORISATION_PROMPT


def test_invoice_extraction_prompt_exists() -> None:
    assert isinstance(prompt_collection.INVOICE_EXTRACTION_PROMPT, str)
    assert "extract the following fields" in prompt_collection.INVOICE_EXTRACTION_PROMPT
