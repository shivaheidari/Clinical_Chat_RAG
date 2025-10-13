import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(

    file_path = "data/NOTEEVENTS_s.csv", 
    content_columns="TEXT"
)

documents = loader.load()

text_spliter = RecursiveCharacterTextSplitter(

    chunk_size=100, 
    chunk_overlap=20
)

split_documents = text_spliter.split_documents(documents)

print(f"Total original documents: {len(documents)}")
print(f"Total chunks created: {len(split_documents)}")
print("\n--- First Chunk (ID 1) ---")
print(f"Content: {split_documents[0].page_content}")
print(f"Metadata: {split_documents[0].metadata}") 