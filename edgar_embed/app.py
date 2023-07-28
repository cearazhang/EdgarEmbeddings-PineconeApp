"""
Ceara Zhang
Streamlit App - Edgar Embeddings
Created: 27 July 2023
Updated: 27 July 2023

app.py:
We need a streamlit app with 5 tabs:
1. Load the Edgar filings from a link (See for example: https://quantopian-archive.netlify.app/notebooks/notebooks/quantopian_notebook_474.html)
2. Compute embeddings: Use sentence transformers to compute embeddings (See https://www.sbert.net/examples/applications/computing-embeddings/README.html)
3. Load embeddings to Pinecone: Upsert embeddings and the text into pinecone (Above examples show how)
4. Ask a question (text tab)
5. Use above examples and langchain to get results.
- a. If answer is known in the earnings call, derive it from there..
- b. Else, give user an option to source it from the web (will tell more later next week)

"""

import streamlit as st
import pandas as pd

def main():
    st.sidebar.title("Streamlit App")
    st.sidebar.subheader("Select a tab:")
    selected_tab = st.sidebar.radio("", ("Load Edgar Filings", "Compute Embeddings", "Load to Pinecone", "Ask a Question", "Get Results"))

    if selected_tab == "Load Edgar Filings":
        load_edgar_filings()
    elif selected_tab == "Compute Embeddings":
        compute_embeddings()
    elif selected_tab == "Load to Pinecone":
        load_to_pinecone()
    elif selected_tab == "Ask a Question":
        ask_question()
    else:
        get_results()

if __name__ == "__main__":
    main()
