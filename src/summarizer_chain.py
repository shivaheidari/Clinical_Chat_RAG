import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# LangChain's Google integrations
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

# --- Configuration ---
CHROMA_PATH = "clinical_reports_db"


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)

embeddings_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

vector_store = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings_model)

retriever = vector_store.as_retriever(search_kwargs={"k": 3})


template = """
You are a specialized Clinical Report Summarizer. Your task is to provide a concise, single-paragraph summary of the patient's status based ONLY on the provided clinical context.

If the context is insufficient to create a summary, state clearly: "Insufficient clinical data to generate a summary."

--- CONTEXT (Clinical Notes):
{context}

--- QUESTION:
{question}

--- CONCISE SUMMARY:
"""
prompt = ChatPromptTemplate.from_template(template)


def format_docs(docs):
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 6. Run the Chain
query = "What were the patient's main reasons for admission and discharge instructions?"
print(f"\n--- Running RAG Chain for Query: {query} ---")


response = rag_chain.invoke(query)

print("\n\n=============== GENERATED SUMMARY ===============")
print(response)
print("=================================================")