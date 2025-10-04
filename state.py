from typing import List, Optional, Any, TypedDict
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage
from utils import FinalResponse, RouterResponse

class AgentState(TypedDict, total=False):
    messages: List[BaseMessage]
    route_decision: RouterResponse
    retrieved_docs: List[Any] 
    agent_response: Optional[str]
    final_response: Optional[FinalResponse]