from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from typing import List, Optional, Any, Literal
from pydantic import BaseModel, Field
from colorama import Fore, Style, init
from ollama._types import ResponseError
from langchain_core.exceptions import OutputParserException
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
import time
from config import LLM_MODEL_NAME, EMBEDDING_MODEL_NAME, LLM_TEMPERATURE



    
def get_llm(model: BaseModel = None, tools: List[Any] = None):
    llm = ChatOllama(model=LLM_MODEL_NAME, temperature=LLM_TEMPERATURE)
    
    if model and tools:
        return llm.bind_tools(tools) 
    elif model:
        return llm.with_structured_output(model)
    elif tools:
        return llm.bind_tools(tools)
    return llm


    
    
def get_embedding_model():
    embedding_model = OllamaEmbeddings(model=EMBEDDING_MODEL_NAME)
    return embedding_model

def invoke_with_retry(chain, payload, state, agent_label, reminder=None, max_attempts=5):
    last_error: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            return chain.invoke(payload)
        except OutputParserException as exc:
            last_error = exc
            print_colored(
                f"{agent_label} structured output error on attempt {attempt}: {exc}",
                "red",
            )
            if attempt == max_attempts:
                break
            if reminder:
                state["messages"].append(HumanMessage(content=reminder))
            time.sleep(3)
        except ResponseError as exc:
            last_error = exc
            print_colored(
                f"{agent_label} API error on attempt {attempt}: {exc}",
                "red",
            )
            if attempt == max_attempts:
                break
            time.sleep(3)
    if last_error:
        raise last_error
    raise RuntimeError(f"{agent_label} failed without returning a response.")


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