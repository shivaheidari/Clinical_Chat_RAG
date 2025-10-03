from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from preprocess import load_pdf, chunk_text

documents = []
for file in Path("../data").glob("*"):
    text = load_pdf(file)
    documents.extend(chunk_text(text))

embeddings = OpenAIEmbeddings()
faiss_index = FAISS.from_texts(documents, embeddings)
faiss_index.save_local("../embeddings/faiss_index")
