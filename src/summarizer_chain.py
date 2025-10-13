import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# LangChain's Google integrations
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

# --- Configuration ---
CHROMA_PATH = "clinical_reports_db"

# 1. Load the LLM (Gemini for Generation)
# We use gemini-2.5-flash for its speed and capability in summarization tasks.
# Assumes GOOGLE_API_KEY is set.
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)

# 2. Load the Retriever (R in RAG)
# We must use the exact same model that created the embeddings!
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# Load the existing, persistent vector store from disk
vector_store = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings_model)

# Convert the vector store to a retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# 3. Define the Prompt Template
# This is the "A" (Augmentation) step. It instructs the LLM how to use the retrieved context.
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


# 4. Define the Document Formatting Function
# This function is used in the LCEL chain to format the retrieved documents 
# into a single string for the prompt's {context} variable.
def format_docs(docs):
    return "\n\n---\n\n".join(doc.page_content for doc in docs)

# 5. Build the LCEL RAG Chain
# LCEL chains use the pipe operator (|) to sequence operations.
rag_chain = (
    # Pass the question to the retriever and the entire input to the rest of the chain
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 6. Run the Chain
query = "What were the patient's main reasons for admission and discharge instructions?"
print(f"\n--- Running RAG Chain for Query: {query} ---")

# .invoke() runs the entire pipeline with a single input
response = rag_chain.invoke(query)

print("\n\n=============== GENERATED SUMMARY ===============")
print(response)
print("=================================================")