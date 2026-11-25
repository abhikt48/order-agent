from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from .tools import llm, TOOLS

SYSTEM = SystemMessage(content=(
"You are a customer support agent. Always look up the order before acting. "
"Use the policy tool for policy questions. For refunds, call issue_refund; "
"a human will approve it. Be brief and never invent order details."
))

llm_with_toools = llm.bind_tool(TOOLS)

def agent(state: MessagesState):
    return {"messages": [llm_with_toools.invoke([SYSTEM] + state["messages"])]}

def build_graph(checkpointer=None):
    g = StateGraph(MessagesState)
    g.add_node("agent", agent)
    g.add_node("tools", ToolNode(TOOLS) )
    g.add_edge(START, "agent")
    g.add_conditional_edges("agent", tools_condition)
    g.add_edge("tools", "agent")
    return g.compile(checkpointer=checkpointer)