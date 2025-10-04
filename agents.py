from utils import get_embedding_model, get_llm, get_final_llm, get_router_llm
from state import AgentState
from prompts import (
    SYSTEM_PROMPT_ROUTER_AGENT,
    SYSTEM_PROMPT_PLANNER_AGENT,
    SYSTEM_PROMPT_FINAL_AGENT,
    SYSTEM_PROMPT_CODE_AGENT,
)

from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


# start agent
def planner_agent(state: AgentState) -> AgentState:
    print("Planner Agent Invoked")
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT_PLANNER_AGENT),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    chain = prompt | llm
    response = chain.invoke({"messages": state["messages"]})
    state["messages"].append(response)
    state["agent_response"] = response.content
    state["planner_plan"] = response.content
    state["agent_last"] = "planner_agent"
    return state


def code_agent(state: AgentState) -> AgentState:
    print("Code Agent Invoked")
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT_CODE_AGENT),
            MessagesPlaceholder(variable_name="messages"),
            (
                "human",
                "Dựa trên kế hoạch và yêu cầu ban đầu, hãy cung cấp mã HTML hoàn chỉnh đáp ứng mô tả.",
            ),
        ]
    )
    chain = prompt | llm
    response = chain.invoke({"messages": state["messages"]})
    state["messages"].append(response)
    state["agent_response"] = response.content
    state["code_output"] = response.content
    state["agent_last"] = "code_agent"
    return state


# end agent
def final_agent(state: AgentState) -> AgentState:
    print("Final Agent Invoked")
    llm = get_final_llm()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT_FINAL_AGENT),
            MessagesPlaceholder(variable_name="messages"),
            (
                "human",
                "Dựa trên toàn bộ hội thoại, hãy tạo câu trả lời cuối cùng cho người dùng và cung cấp mã HTML đã tổng hợp.",
            ),
        ]
    )
    chain = prompt | llm
    response = chain.invoke({"messages": state["messages"]})
    state["final_response"] = response
    state["agent_last"] = "final_agent"

    summary_chunks = []
    if response.message:
        summary_chunks.append(response.message)
    if response.html:
        summary_chunks.append(f"HTML Output:\n{response.html}")
    if summary_chunks:
        state["messages"].append(AIMessage(content="\n\n".join(summary_chunks)))
    return state


def router_agent(state: AgentState) -> AgentState:
    print("Router Agent Invoked")
    llm = get_router_llm()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT_ROUTER_AGENT),
            MessagesPlaceholder(variable_name="messages"),
            (
                "human",
                "Agent vừa hoàn thành: {agent_last}. Dựa trên tiến trình hiện tại, hãy quyết định agent tiếp theo cần thực hiện và giải thích ngắn gọn.",
            ),
        ]
    )
    chain = prompt | llm
    response = chain.invoke(
        {
            "messages": state["messages"],
            "agent_last": state.get("agent_last", "unknown"),
        }
    )
    state["route_decision"] = response
    decision_summary = (
        f"Router quyết định chuyển từ {response.agent_current} sang {response.next_agent}."
    )
    if response.reason:
        decision_summary += f" Lý do: {response.reason}"
    state["messages"].append(AIMessage(content=decision_summary))
    state["agent_last"] = "router_agent"
    return state
