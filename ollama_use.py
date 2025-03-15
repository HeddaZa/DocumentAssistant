import streamlit as st
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate

# Initialize Ollama model
llm = OllamaLLM(model="llama3.2")

# Create a prompt template for spell-checking
spell_check_prompt = PromptTemplate(
    input_variables=["text"],
    template="Please spell-check and correct the following text: {text}"
)

# Create an LLMChain for spell-checking
spell_check_chain = spell_check_prompt|llm

test_text = "I am a good speler."
result = spell_check_chain.invoke({"text":test_text})
print(result)

# Streamlit UI
# st.title("Spell-Check App")

# # Text input
# user_text = st.text_area("Enter text to spell-check:", height=200)

# if st.button("Spell-Check"):
#     if user_text:
#         # Run spell-check
#         result = spell_check_chain.run(user_text)
        
#         # Display result
#         st.subheader("Corrected Text:")
#         st.write(result)
#     else:
#         st.warning("Please enter some text to spell-check.")
