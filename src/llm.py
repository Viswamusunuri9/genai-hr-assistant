# from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

def get_llm():
    return ChatOpenAI(temperature=0)