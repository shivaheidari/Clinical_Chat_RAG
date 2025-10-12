import os
import openai
from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found. Please check your .env file.")



llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
messages = [
    HumanMessage(content="Explain the LangChain Expression Language (LCEL) in one sentence.", temprature=0.7)
]

print("--- LLM Response ---")
response = llm.invoke(messages)

print(response.content)