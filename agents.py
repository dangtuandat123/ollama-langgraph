from utils import get_embedding_model,get_llm,get_final_llm,get_router_llm
from state import AgentState
from prompts import SYSTEM_PROMPT_ROUTER_AGENT, SYSTEM_PROMPT_PLANNER_AGENT, SYSTEM_PROMPT_FINAL_AGENT, SYSTEM_PROMPT_CODE_AGENT

from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

#start agent
def planner_agent(state: AgentState) -> AgentState:
    print("Planner Agent Invoked")
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages(
        [
            ('system', SYSTEM_PROMPT_PLANNER_AGENT),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    chain = prompt | llm
    response = chain.invoke({"messages": state["messages"]})
    state["agent_response"] = response.content
    return state


def code_agent(state: AgentState) -> AgentState:
    print("Code Agent Invoked")
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages(
        [
            ('system', SYSTEM_PROMPT_CODE_AGENT),
            ('human', "Dựa trên thông tin sau, viết mã nguồn để giải quyết yêu cầu: {messages}"),
        ]
    )
    chain = prompt | llm
    response = chain.invoke({"messages": state["agent_response"]})
    state["messages"].append(response)
    state["agent_response"] = response.content
    return state
    
#end agent
def final_agent(state: AgentState) -> AgentState:
    print("Final Agent Invoked")
    llm = get_final_llm()
    prompt = ChatPromptTemplate.from_messages(
        [
            ('system', SYSTEM_PROMPT_FINAL_AGENT),
            ('human', "Dựa trên thông tin sau, cung cấp câu trả lời cuối cùng cho người dùng: {messages}"),
        ]
    )
    chain = prompt | llm
    response = chain.invoke({"messages": state["agent_response"]})
    state["final_response"] = response
    return state


def router_agent(state: AgentState) -> AgentState:
    print("Router Agent Invoked")
    llm = get_router_llm()
    prompt = ChatPromptTemplate.from_messages(
        [
            ('system', SYSTEM_PROMPT_ROUTER_AGENT),
            ('human', "Dựa trên thông tin sau, quyết định agent tiếp theo cần thực hiện: {messages}"),
        ]
    )
    chain = prompt | llm
    response = chain.invoke({"messages": state["agent_response"]})
    state["route_decision"] = response
    return state