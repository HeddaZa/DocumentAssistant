from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

# Initialize Ollama model
llm = OllamaLLM(model="gemma")

# Create a prompt template for spell-checking
spell_check_prompt = PromptTemplate(
    input_variables=["text"],
    template="Please spell-check and correct the following text: {text}",
)

# Create an LLMChain for spell-checking
spell_check_chain = spell_check_prompt | llm

test_text = "I am a good speler."
result = spell_check_chain.invoke({"text": test_text})
