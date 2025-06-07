CATEGORISATION_PROMPT = """
You are an expert in categorizing text. The text can be receipts or a results
from a doctor, or any other type of document.
Details about the categories are at the end of the prompt.
The text is: {text}

Gib nur Informationen an, die auch tatsächlich im Text vorkommen.
"""

INVOICE_EXTRACTION_PROMPT = """
    You are an expert at extracting information from invoices and receipts.
    Given the following text, extract the following fields:
    - type: The type of invoice (receipt_from_doctor, \
      receipt_for_stationery, receipt_for_flat, other)
    - price: The total price or amount on the invoice
    - date: The date of the invoice
    - description: A short description of the invoice
    - notes: Any additional notes
    - logs: A list of log entries, each with a log string and a date
    Return the result as a JSON object matching the expected schema.
    """
