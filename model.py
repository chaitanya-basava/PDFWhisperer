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
    GEMMA_2_9B = "gemma2-9b-it"
    MISTRAL_7B_INSTRUCT = "mistralai/mistral-7b-instruct:free"
    GROQ_LLAMA_3_1 = "llama-3.1-70b-versatile"

    @staticmethod
    def get_llm_by_id(llm_id: int):
        llm_mapping = {
            1: LLM.LLAMA_3_8B,
            2: LLM.COHERE_COMMAND_R,
            3: LLM.GEMMA_2_9B,
            4: LLM.MISTRAL_7B_INSTRUCT,
            5: LLM.GROQ_LLAMA_3_1
        }

        return llm_mapping[llm_id]

    @staticmethod
    def __openrouter_models():
        return {LLM.LLAMA_3_8B, LLM.MISTRAL_7B_INSTRUCT}

    @staticmethod
    def __groq_models():
        return {LLM.GEMMA_2_9B, LLM.GROQ_LLAMA_3_1}

    @staticmethod
    def get_llm(model_name) -> BaseChatModel:
        if model_name == LLM.COHERE_COMMAND_R:
            return ChatCohere(model_name=str(model_name.value))
        elif model_name in LLM.__openrouter_models():
            return ChatOpenRouter(model_name=str(model_name.value))
        elif model_name in LLM.__groq_models():
            return ChatGroq(model_name=str(model_name.value))

        raise Exception("Model not supported")


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
