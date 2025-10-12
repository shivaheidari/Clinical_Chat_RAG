import streamlit as st
from retrieve import query_faiss
from generate import generate_answer

st.title("Domain FAQ Assistant")
query = st.text_input("Ask a question:")

if query:
    docs = query_faiss(query)
    answer = generate_answer(query, docs)
    st.write("**Answer:**", answer)
    st.write("**Sources:**", docs)
