import streamlit as st
from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Initialize Ollama model
llm = Ollama(model="llama3.2")

# Create a prompt template for spell-checking
spell_check_prompt = PromptTemplate(
    input_variables=["text"],
    template="Please spell-check and correct the following text: {text}"
)

# Create an LLMChain for spell-checking
spell_check_chain = LLMChain(llm=llm, prompt=spell_check_prompt)

# Streamlit UI
st.title("Spell-Check App")

# Text input
user_text = st.text_area("Enter text to spell-check:", height=200)

if st.button("Spell-Check"):
    if user_text:
        # Run spell-check
        result = spell_check_chain.run(user_text)
        
        # Display result
        st.subheader("Corrected Text:")
        st.write(result)
    else:
        st.warning("Please enter some text to spell-check.")
