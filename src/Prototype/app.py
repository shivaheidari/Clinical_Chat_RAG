import os
import openai
from dotenv import find_dotenv, load_dotenv
from langchain_community.llms import OpenAI

load_dotenv(find_dotenv())
openai.api_key = os.getenv("Key")

llm_model = "gpt-3.5-turbo"
llm = OpenAI(openai_api_key = os.getenv("Key"))

