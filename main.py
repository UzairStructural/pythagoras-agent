import streamlit as st
from gpt_engine import ask_gpt_with_memory
from memory_store import store_embedding, retrieve_similar_chunks

st.title("Pythagoras - Project Management Agent")

uploaded_file = st.file_uploader("Upload RFI, Spec, or Decision Note")
query = st.text_area("Ask a question or provide context")

if st.button("Submit"):
    if uploaded_file:
        content = uploaded_file.read().decode("utf-8")
        store_embedding(content)  # Save to vector DB
        st.success("Memory stored")

    if query:
        relevant_chunks = retrieve_similar_chunks(query)
        response = ask_gpt_with_memory(query, relevant_chunks)
        st.markdown("### 🧠 Agent Response")
        st.write(response)
