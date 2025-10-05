from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from typing import List, Optional, Any, Literal
from pydantic import BaseModel, Field
from colorama import Fore, Style, init

from config import LLM_MODEL_NAME, EMBEDDING_MODEL_NAME, LLM_TEMPERATURE


class FinalResponse(BaseModel):
    message: Optional[str] = Field(description="Lời giải thích ngắn gọn, thân thiện dành cho người dùng.")
    html: Optional[str] = Field(description="Nội dung HTML.")
   
class RouterResponse(BaseModel):
    agent_current: Literal["planner_agent", "code_agent", "final_agent", "router_agent"] = Field(description="agent hiện tại đang thực thi.")
    next_agent: Literal["final_agent", "code_agent"] = Field(description="agent tiếp theo sẽ thực hiện.")
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

def print_colored(text: str, color: str = "green") -> None:

    init(autoreset=True) 

    color_dict = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE,
    }

    chosen_color = color_dict.get(color.lower(), Fore.GREEN) 
    print(f"{chosen_color}{text}{Style.RESET_ALL}")