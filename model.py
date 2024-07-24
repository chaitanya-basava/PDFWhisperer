import os
from enum import Enum
from typing import Optional
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_cohere.chat_models import ChatCohere
from langchain_community.chat_models import ChatOpenAI
from langchain_core.language_models import BaseChatModel

print(load_dotenv(".env"))


class LLM(Enum):
    LLAMA_3_8B = "meta-llama/llama-3-8b-instruct:free"
    COHERE_COMMAND_R = "command-r-plus"
    GEMMA_3_9B = "google/gemma-2-9b-it:free"
    MISTRAL_7B_INSTRUCT = "mistralai/mistral-7b-instruct:free"
    GROQ_LLAMA_3_1 = "llama-3.1-70b-versatile"

    @staticmethod
    def openrouter_models():
        return {LLM.LLAMA_3_8B, LLM.GEMMA_3_9B, LLM.MISTRAL_7B_INSTRUCT}


class ChatOpenRouter(ChatOpenAI):
    openai_api_base: str
    openai_api_key: str
    model_name: str

    def __init__(self,
                 model_name: str,
                 openai_api_key: Optional[str] = None,
                 openai_api_base: str = "https://openrouter.ai/api/v1",
                 **kwargs):
        openai_api_key = openai_api_key or os.getenv('OPENROUTER_API_KEY')
        super().__init__(openai_api_base=openai_api_base,
                         openai_api_key=openai_api_key,
                         model_name=model_name, **kwargs)


class LLMBuilder:
    @staticmethod
    def get_llm(model_name: LLM) -> BaseChatModel:
        if model_name == LLM.COHERE_COMMAND_R:
            return ChatCohere(model_name=str(model_name.value))
        elif model_name in LLM.openrouter_models():
            return ChatOpenRouter(model_name=str(model_name.value))
        elif model_name == LLM.GROQ_LLAMA_3_1:
            return ChatGroq(model_name=str(model_name.value))

        raise Exception("Model not supported")
