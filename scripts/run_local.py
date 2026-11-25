from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from app.graph import build_graph

graph = build_graph(InMemorySaver())

cfg1 = {"configurable": {
    "thread_id": "demo-1"
}}


r = graph.invoke(
    {"messages": [("user", "Where is order 1001?")]}, cfg1)

print(r["messages"][-1].content)

r = graph.invoke(
    {
        "messages": [
            ("user", "What's your return policy?")
        ]
    },
    {
        "configurable": {
            "thread_id": "demo-2"
        }
    }
)

print(r["messages"][-1].content)

cfg3 = {
    "configurable": {
        "thread_id": "demo-3"
    }
}

r = graph.invoke(
    {
        "messages": [
            ("user", "Order 1002 arrived damaged, I want a refund")
        ]
    },
    cfg3
)

print("PAUSED:", r.get("__interrupt__"))

r = graph.invoke(
    Command(resume="approve"),
    cfg3
)

print(r["messages"][-1].content)