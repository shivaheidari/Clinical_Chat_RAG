import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.document_loaders import CSVLoader
import os
import json 

#----------configuration------------
out_put_path = "data/clinical_chunks.json"
chunk_size = 100
chunk_overlap = 20

loader = CSVLoader(

    file_path = "data/NOTEEVENTS_s.csv", 
    content_columns="TEXT"
)

documents = loader.load()

text_spliter = RecursiveCharacterTextSplitter(

    chunk_size=chunk_size, 
    chunk_overlap=chunk_overlap
)

split_documents = text_spliter.split_documents(documents)

data_to_save = [{"page_content": doc.page_content, "metadata":doc.metadata} 
                for doc in split_documents]

os.makedirs(os.path.dirname(out_put_path), exist_ok=True)

with open(out_put_path, 'w', encoding='utf-8') as f:
    json.dump(data_to_save, f, ensure_ascii=False, indent=4)