from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(model_name="gpt-3.5-turbo")

def generate_answer(query, retrieved_docs):
    context = "\n\n".join(retrieved_docs)
    prompt = f"""
    You are an assistant. Use the context below to answer the question.
    
    Context:
    {context}
    
    Question:
    {query}
    Answer:
    """
    response = llm(prompt)
    return response
