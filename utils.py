from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from typing import List, Optional, Any, Literal
from pydantic import BaseModel, Field

from config import LLM_MODEL_NAME, EMBEDDING_MODEL_NAME, LLM_TEMPERATURE


class FinalResponse(BaseModel):
    message: Optional[str] = Field(description="Lời giải thích ngắn gọn, thân thiện dành cho người dùng.")
    html: Optional[str] = Field(description="Nội dung HTML.")
   
class RouterResponse(BaseModel):
    agent_current: Literal["code_agent", "final_agent"] = Field(description="agent_current")
    next_agent: Literal["final_agent", "code_agent"] = Field(description="next_agent")
    reason: Optional[str] = Field(description="Lý do chuyển đổi agent, nếu có.")

def get_llm():
    llm = ChatOllama(model=LLM_MODEL_NAME, temperature=LLM_TEMPERATURE)
    return llm

def get_final_llm():
    llm = ChatOllama(model=LLM_MODEL_NAME, temperature=0)
    return llm.with_structured_output(FinalResponse)

def get_router_llm():
    llm = ChatOllama(model=LLM_MODEL_NAME, temperature=0)
    return llm.with_structured_output(RouterResponse)

def get_embedding_model():
    embedding_model = OllamaEmbeddings(model=EMBEDDING_MODEL_NAME)
    return embedding_model