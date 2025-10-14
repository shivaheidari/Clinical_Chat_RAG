import json
import os
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings 
from langchain_community.vectorstores import Chroma

from dotenv import load_dotenv

load_dotenv()


# --- Configuration (must match dataloading.py) ---
INPUT_JSON_PATH = "data/clinical_chunks.json"
CHROMA_PATH = "clinical_reports_db"

try:
    with open(INPUT_JSON_PATH, 'r', encoding='utf-8') as f:
        data_loaded = json.load(f)

    # Convert the list of dicts back into LangChain Document objects
    reconstructed_documents = [
        Document(page_content=item['page_content'], metadata=item['metadata'])
        for item in data_loaded
    ]
    print(f"Successfully reconstructed {len(reconstructed_documents)} LangChain Documents.")
except FileNotFoundError:
    print(f"Error: {INPUT_JSON_PATH} not found. Did you run dataloading.py first?")
    exit()
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
print("Gemini Embeddings model initialized.")

vector_store = Chroma.from_documents(
    documents=reconstructed_documents,
    embedding=embeddings_model,
    persist_directory=CHROMA_PATH
)
vector_store.persist()